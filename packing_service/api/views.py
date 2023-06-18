import csv
from random import choice

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils.filter_order import read_csv_file
from .utils.order_and_cancel import cancel_order, get_order_by_id
from .utils.parse_order_id import get_orderkey


class OrdersView(APIView):
    """
    Класс представления для получения информации о заказе.
    """

    FILE_PATH = 'data/data.csv'
    SKU_FILE_PATH = 'data/sku.csv'
    SKU_CARGOTYPES_FILE_PATH = 'data/sku_cargotypes.csv'

    barcodes = []

    def get(self, request):
        """
        Метод GET для получения информации о заказе.
        """
        self.barcodes = request.GET.getlist('barcode')
        filtered_data = read_csv_file(
            self.FILE_PATH,
            self.SKU_FILE_PATH,
            self.SKU_CARGOTYPES_FILE_PATH,
            choice(get_orderkey())
        )

        if filtered_data:
            return Response(filtered_data)
        else:
            return Response({'error': 'Заказ не найден'})

    def post(self, request):
        """
        Метод POST для получения информации о заказе с передачей баркодов.
        """
        order_number = request.data.get('orderkey')
        barcodes = request.data.get('barcodes')

        return Response({'message': 'POST-запрос успешно обработан.'})
    
    def patch(self, request):
        order_id = request.data.get('orderkey')

        order = get_order_by_id(order_id)
        if not order:
            return Response({'error': 'Заказ не найден'}, status=status.HTTP_404_NOT_FOUND)

        cancel_order(order_id)

        return Response({'message': 'Заказ успешно отменен'})


class PackageView(APIView):
    """
    Класс представления обработки операций, связанных с упаковкой товаров.
    """

    FILE_PATH = 'data/data.csv'
    SKU_FILE_PATH = 'data/sku.csv'
    SKU_CARGOTYPES_FILE_PATH = 'data/sku_cargotypes.csv'

    def get_order_list(self, orderkey):
        """
        Получение списка товаров для заданного ключа заказа.
        """
        order_list = list(csv.reader(open(self.FILE_PATH)))
        return [el for el in order_list[1:] if el[2] == orderkey]

    def get_sku_info_dict(self):
        """
        Получение словаря информации о товарах.
        """
        sku_list = list(csv.reader(open(self.SKU_FILE_PATH)))
        cargotypes = list(csv.reader(open(self.SKU_CARGOTYPES_FILE_PATH)))

        sku_info_dict = {}
        sku_info_dict2 = {}

        for row in sku_list[1:]:
            sku_info_dict[row[1]] = {
                'size1': row[2],
                'size2': row[3],
                'size3': row[4],
                'type': []
            }
            sku_info_dict2[row[1]] = {
                'name': row[6],
                'pic': row[7],
                'barcode': row[5]
            }
        for row in cargotypes[1:]:
            if row[1] in sku_info_dict:
                sku_info_dict[row[1]].setdefault('type', []).append(row[2])

        return sku_info_dict, sku_info_dict2

    def build_items_list(self, sku, count_weight_dict, sku_info_dict):
        """
        Построение списка товаров для упаковки.
        """
        items_list = []
        sku_set = set()

        for el in sku:
            if el not in sku_set:
                temp_dict = sku_info_dict[el].copy()
                temp_dict['sku'] = el
                temp_dict['count'] = count_weight_dict[el]['count']
                temp_dict['weight'] = count_weight_dict[el]['weight']
                items_list.append(temp_dict)
                sku_set.add(el)

        return items_list

    def build_order_after_ml(self, orderkey, data, count_weight_dict, sku_info_dict, sku_info_dict2):
        """
        Построение данных о заказе после обработки моделью машинного обучения.
        """
        order_after_ml = {
            'orderId': orderkey,
            'packages': []
        }

        package_id = 1

        sku_counts = {}
        for package_data in data.get('package', []):
            for sku, recommended_packs in package_data.items():
                count = count_weight_dict[sku]['count']
                if sku in sku_counts:
                    if count > sku_counts[sku]['count']:
                        sku_counts[sku] = {
                            'count': count,
                            'package': package_data,
                        }
                else:
                    sku_counts[sku] = {
                        'count': count,
                        'package': package_data,
                    }

        for sku, package_data in sku_counts.items():
            package = {
                'packageId': package_id,
                'recommendedPacks': package_data['package'][sku],
                'items': []
            }

            item = sku_info_dict[sku].copy()
            item.update(sku_info_dict2[sku])
            item['sku'] = sku
            item['count'] = package_data['count']
            item['weight'] = count_weight_dict[sku]['weight']
            package['items'].append(item)

            order_after_ml['packages'].append(package)

            package_id += 1

        return order_after_ml

    def get(self, request, orderkey: str):
        """
        Обработка GET-запроса для получения информации об упаковке для заданного ключа заказа.
        """
        order_list = self.get_order_list(orderkey)
        sku_info_dict, sku_info_dict2 = self.get_sku_info_dict()

        order = []
        sku = set()

        for el in order_list:
            order.append(el)
            sku.add(el[12])

        count_weight_dict = {}

        for el in sku:
            count_weight_dict[el] = {'count': 0}

        for el in order:
            count_weight_dict[el[12]]['count'] += 1
            count_weight_dict[el[12]]['weight'] = el[11]

        items_list = self.build_items_list(sku, count_weight_dict, sku_info_dict)

        request_dict = {
            'orderId': orderkey,
            'items': items_list,
        }

        result = requests.post('http://localhost:8001/pack', json=request_dict)
        if result.status_code == 200:
            data = result.json()
            order_after_ml = self.build_order_after_ml(orderkey, data, count_weight_dict, sku_info_dict, sku_info_dict2)

            return Response(order_after_ml)

        else:
            return Response({'error': 'Failed to retrieve data'}, status=result.status_code)
