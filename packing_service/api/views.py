from rest_framework.response import Response
from rest_framework.views import APIView

from .utils.csv_utils import read_csv_file


class OrdersView(APIView):  
    def get(self, request, orderkey):
        file_path = 'E:/dev/project/proj_yandex/packing_service/data/data2.csv'
        filtered_data = read_csv_file(file_path, orderkey)
    
        if filtered_data:
            return Response(filtered_data)
        else:
            return Response({'error': 'Заказ не найден'})





class SkuView(APIView):
    def post(self, request):
        identifiers = request.data
        file_path = 'E:/dev/project/proj_yandex/packing_service/data/sku2.csv'
        
        results = []
        
        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            
            for row in reader:
                if row[1] in identifiers:
                    data = {
                        '': row[0],
                        'sku': row[1],
                        'a': row[2],
                        'b': row[3],
                        'c': row[4]
                    }
                    results.append(data)
        
        if results:
            return Response(results)
        
        return Response({'error': 'Товары не найдены или не существуют'})

