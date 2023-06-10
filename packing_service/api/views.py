import csv

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework.views import APIView


class OrdersView(APIView):
    @swagger_auto_schema(
        responses={
            200: openapi.Response(
                description='Successful response',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'whs': openapi.Schema(type=openapi.TYPE_STRING),
                        'orderkey': openapi.Schema(type=openapi.TYPE_STRING),
                        'selected_cartontype': openapi.Schema(type=openapi.TYPE_STRING),
                        'box_num': openapi.Schema(type=openapi.TYPE_STRING),
                        'recommended_cartontype': openapi.Schema(type=openapi.TYPE_STRING),
                        'selected_carton': openapi.Schema(type=openapi.TYPE_STRING),
                        'sel_calc_cube': openapi.Schema(type=openapi.TYPE_STRING),
                        'recommended_carton': openapi.Schema(type=openapi.TYPE_STRING),
                        'pack_volume': openapi.Schema(type=openapi.TYPE_STRING),
                        'rec_calc_cube': openapi.Schema(type=openapi.TYPE_STRING),
                        'goods_wght': openapi.Schema(type=openapi.TYPE_STRING),
                        'sku': openapi.Schema(type=openapi.TYPE_STRING),
                        'who': openapi.Schema(type=openapi.TYPE_STRING),
                        'trackingid': openapi.Schema(type=openapi.TYPE_STRING),
                    },
                    example={
                        'whs': 6,
                        'orderkey': 'd48f3211c1ffccdc374f23139a9ab668',
                        'selected_cartontype': 'NONPACK',
                        'box_num': 1,
                        'recommended_cartontype': 'YML',
                        'selected_carton': 'NONPACK',
                        'sel_calc_cube': 0,
                        'recommended_carton': 'YML',
                        'pack_volume': 2046,
                        'rec_calc_cube': 108000,
                        'goods_wght': 0.1,
                        'sku': 'af49bf330e2cf16e44f0be1bdfe337bd',
                        'who': 'b7325da1af89a46059164618eb03ae38',
                        'trackingid': '6c304d5c2815ccd2ba5046c101294c24',
                    }
                )
            ),
            404: 'Order not found'
        }
    )
    
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


class MergeDataAPIView(APIView):
    def get(self, request):
        data_file_path = 'E:/dev/project/proj_yandex/packing_service/data/data2.csv'
        sku_file_path = 'E:/dev/project/proj_yandex/packing_service/data/sku2.csv'
        cargotype_file_path = 'E:/dev/project/proj_yandex/packing_service/data/sku_cargotypes2.csv'
        
        merged_data = merge_data(data_file_path, sku_file_path, cargotype_file_path)
        
        return Response(merged_data)

def merge_data(data_file_path, sku_file_path, cargotype_file_path):
    data = []
    sku_data = {}
    cargotype_data = {}
    
    with open(sku_file_path, 'r', newline='') as sku_file:
        sku_reader = csv.DictReader(sku_file, delimiter=',')
        for row in sku_reader:
            sku_data[row['sku']] = {
                'a': row['a'],
                'b': row['b'],
                'c': row['c']
            }
    
    with open(cargotype_file_path, 'r', newline='') as cargotype_file:
        cargotype_reader = csv.DictReader(cargotype_file, delimiter=',')
        for row in cargotype_reader:
            sku = row['sku']
            cargotype = row['cargotype']
            if sku in cargotype_data:
                cargotype_data[sku].append(cargotype)
            else:
                cargotype_data[sku] = [cargotype]
    
    with open(data_file_path, 'r', newline='') as data_file:
        data_reader = csv.DictReader(data_file, delimiter=',')
        for row in data_reader:
            sku = row['sku']
            if sku in sku_data:
                row['a'] = sku_data[sku]['a']
                row['b'] = sku_data[sku]['b']
                row['c'] = sku_data[sku]['c']
            
            if sku in cargotype_data:
                row['cargotypes'] = cargotype_data[sku]
            
            data.append(row)
    
    return data