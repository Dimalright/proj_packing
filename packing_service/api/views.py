import csv
from random import choice

import requests
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils.filter_order import read_csv_file
from .utils.parse_order_id import get_orderkey
from .utils.process_package import process_package_data


class OrdersView(APIView):
    """
    Класс представления для получения информации о заказе.
    """

    file_path = 'data/data.csv'
    sku_file_path = 'data/sku.csv'
    sku_cargotypes_file_path = 'data/sku_cargotypes.csv'

    def get(self, request):
        """
        Метод GET для получения информации о заказе.
        """
        barcodes = request.GET.getlist('barcode')
        filtered_data = read_csv_file(
            self.file_path,
            self.sku_file_path,
            self.sku_cargotypes_file_path,
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


class PackageView(APIView):
    """
    API endpoint для обработки заказа и создания упаковок.
    """

    def get(self, request, orderkey: str):
        order_list = []
        sku_list = []
        cargotypes = []

        with open('data/data.csv') as order_file:
            order_list = list(csv.reader(order_file))

        with open('data/sku.csv') as sku_file:
            sku_list = list(csv.reader(sku_file))

        with open('data/sku_cargotypes.csv') as cargotypes_file:
            cargotypes = list(csv.reader(cargotypes_file))

        order = []
        sku = set()

        for el in order_list[1:]:
            if el[2] == orderkey:
                order.append(el)
                sku.add(el[12])

        count_weight_dict = {}

        for el in order:
            sku_code = el[12]
            if sku_code not in count_weight_dict:
                count_weight_dict[sku_code] = {'count': 0}
            count_weight_dict[sku_code]['count'] += 1
            count_weight_dict[sku_code]['weight'] = el[11]

        sku_info_dict = {}

        for row in sku_list[1:]:
            sku_info_dict[row[1]] = {
                'size1': row[2],
                'size2': row[3],
                'size3': row[4],
                'type': [],
                'name': row[6],
                'pic': row[7],
                'barcode': row[5]
            }

        for row in cargotypes[1:]:
            if row[1] in sku_info_dict:
                sku_info_dict[row[1]].setdefault('type', []).append(row[2])

        items_list = []

        for sku_code in sku:
            if sku_code not in items_list:
                temp_dict = sku_info_dict[sku_code].copy()
                temp_dict['sku'] = sku_code
                temp_dict['count'] = count_weight_dict[sku_code]['count']
                temp_dict['weight'] = count_weight_dict[sku_code]['weight']
                items_list.append(temp_dict)

        request_dict = {
            'orderId': orderkey,
            'items': items_list
        }

        result = requests.post('http://localhost:8001/pack', json=request_dict)

        if result.status_code == 200:
            data = result.json()

            order_after_ml = process_package_data(data, count_weight_dict, sku_info_dict)

            return Response(order_after_ml)
        else:
            return Response({'error': 'Failed to retrieve data'}, status=result.status_code)
