import csv
import json
import pprint
from random import choice

import requests
from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils.csv_utils import read_csv_file
from .utils.parse_order_id import get_orderkey


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
        # print(order_number, barcodes)

        # Здесь можно обработать полученные баркоды и выполнить необходимую логику

        return Response({'message': 'POST-запрос успешно обработан.'})





class PackageView(APIView):
    def get(self, request, orderkey: str):
        order_list = list(csv.reader(open('data/data.csv')))
        sku_list = list(csv.reader(open('data/sku.csv')))
        cargotypes = list(csv.reader(open('data/sku_cargotypes.csv')))

        order = []
        sku = set()

        for el in order_list[1:]:
            if el[2] == orderkey:
                order.append(el)
                sku.add(el[12])

        count_weight_dict = {}

        for el in sku:
            count_weight_dict[el] = {'count': 0}

        for el in order:
            count_weight_dict[el[12]]['count'] += 1
            count_weight_dict[el[12]]['weight'] = el[11]

        items_list = []

        for el in sku:
            temp_dict = {}
            for row in sku_list[1:]:
                if row[1] == el:
                    temp_dict = {
                        'sku': el,
                        'size1': row[2],
                        'size2': row[3],
                        'size3': row[4],
                        'type': []
                    }
                    break
            for row in cargotypes[1:]:
                if row[1] == el:
                    temp_dict.setdefault('type', []).append(row[2])
            temp_dict['count'] = count_weight_dict[el]['count']
            temp_dict['weight'] = count_weight_dict[el]['weight']
            items_list.append(temp_dict)

        request_dict = {
            'orderId': orderkey,
            'items': items_list
        }
        print(items_list)
        result = requests.post('http://localhost:8001/pack', json=request_dict)

        if result.status_code == 200:
            data = result.json()
            orderAfterML = {
                'orderId': orderkey,
                'packages': []
            }

        for i, package_data in enumerate(data.get('package', []), 1):
            package = {
                'packageId': i,
                'recommendedPacks': None,
                'items': []
            }
            for package_id, recommended_packs in package_data.items():
                package['recommendedPacks'] = recommended_packs

            for item in items_list:
                package['items'].append(item.copy())

            orderAfterML['packages'].append(package)

            sku_info_dict = {}
            for row in sku_list[1:]:
                sku_info_dict[row[1]] = {
                    'name': row[6],
                    'pic': row[7]
                }

            for package in orderAfterML['packages']:
                for item in package['items']:
                    sku = item['sku']
                    name = sku_info_dict[sku]['name']
                    item['name'] = name
                    item['pic'] = sku_info_dict[sku]['pic']

            return HttpResponse(json.dumps(orderAfterML, ensure_ascii=False))

        else:
            return JsonResponse({'error': 'Failed to retrieve data'}, status=result.status_code)