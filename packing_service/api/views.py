from random import choice

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
