from random import choice

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils.build_item_list import build_items_list
from .utils.build_order_after_ml import build_order_after_ml
from .utils.filter_order import read_csv_file
from .utils.order_and_cancel import cancel_order, get_order_by_id
from .utils.order_list import get_order_list
from .utils.parse_order_id import get_orderkey
from .utils.sku_info import get_sku_info_dict


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

    def get(self, request, orderkey: str):
        """
        Обработка GET-запроса для получения информации об упаковке для заданного ключа заказа.
        """
        order_list = get_order_list(self, orderkey)
        sku_info_dict, sku_info_dict2 = get_sku_info_dict(self)

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

        items_list = build_items_list(self, sku, count_weight_dict, sku_info_dict)

        request_dict = {
            'orderId': orderkey,
            'items': items_list,
        }

        result = requests.post('http://localhost:8001/pack', json=request_dict)
        if result.status_code == 200:
            data = result.json()
            order_after_ml = build_order_after_ml(self, orderkey, data, count_weight_dict, sku_info_dict, sku_info_dict2)

            return Response(order_after_ml)

        else:
            return Response({'error': 'Failed to retrieve data'}, status=result.status_code)
