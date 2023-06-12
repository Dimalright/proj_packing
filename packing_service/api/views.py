from rest_framework.response import Response
from rest_framework.views import APIView

from .utils.csv_utils import read_csv_file


class OrdersView(APIView):
    """
    Класс представления для получения информации о заказе.
    """

    file_path = 'data/data2.csv'
    sku2_file_path = 'data/sku2.csv'
    sku_cargotypes2_file_path = 'data/sku_cargotypes2.csv'

    def get(self, request, orderkey):
        """
        Метод GET для получения информации о заказе.
        """

        filtered_data = read_csv_file(
            self.file_path,
            self.sku2_file_path,
            self.sku_cargotypes2_file_path,
            orderkey
        )

        if filtered_data:
            return Response(filtered_data)
        else:
            return Response({'error': 'Заказ не найден'})
