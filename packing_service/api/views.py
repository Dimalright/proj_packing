import csv

from rest_framework.response import Response
from rest_framework.views import APIView


class OrdersView(APIView):
    def get(self, request, orderkey):
        file_path = 'E:/dev/project/proj_yandex/packing_service/data/data2.csv'
        filtered_data = read_csv_file(file_path, orderkey)
    
        if filtered_data:
            return Response(filtered_data)
        else:
            return Response({'error': 'Заказ не найден'})
    


def read_csv_file(file_path, orderkey):
    data = []
    count = 0

    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            if row.get('orderkey') == orderkey:
                data.append(row)       
    return data



class SkuView(APIView):
    def get(self, request, sku):
        file_path = 'E:/dev/project/proj_yandex/packing_service/data/sku2.csv'
        
        with open(file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            
            for row in reader:
                if row[1] == sku:
                    data = {
                        'sku': row[1],
                        'a': row[2],
                        'b': row[3],
                        'c': row[4]
                    }
                    return Response(data)
        
        return Response({'error': 'Файл не найден или товар не существует'})