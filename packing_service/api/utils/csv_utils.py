import csv


def read_csv_file(file_path, orderkey):
    data = []
    orderkey_count = {} 

    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            orderkey_count[row['orderkey']] = orderkey_count.get(row['orderkey'], 0) + 1
            if row.get('orderkey') == orderkey:
                item = {
                    '': int(row['']),
                    'count': orderkey_count[row['orderkey']],
                    'whs': int(row['whs']),
                    'orderkey': row['orderkey'],
                    'selected_cartontype': row['selected_cartontype'],
                    'box_num': int(row['box_num']),
                    'recommended_cartontype': row['recommended_cartontype'],
                    'selected_carton': row['selected_carton'],
                    'sel_calc_cube': float(row['sel_calc_cube']),
                    'recommended_carton': row['recommended_carton'],
                    'pack_volume': float(row['pack_volume']),
                    'rec_calc_cube': float(row['rec_calc_cube']),
                    'goods_wght': float(row['goods_wght']) if row['goods_wght'] else None,
                    'sku': row['sku'],
                    'who': row['who'],
                    'trackingid': row['trackingid'],
                    'a': None,
                    'b': None,
                    'c': None,
                    'cargotype': [],
                }
                data.append(item)

    sku2_file_path = 'E:/dev/project/proj_yandex/packing_service/data/sku2.csv'
    with open(sku2_file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        sku_data = {row['sku']: {'a': float(row['a']), 'b': float(row['b']), 'c': float(row['c'])} for row in reader}

    sku_cargotypes2_file_path = 'E:/dev/project/proj_yandex/packing_service/data/sku_cargotypes2.csv'
    with open(sku_cargotypes2_file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        cargotype_data = {}
        for row in reader:
            sku = row['sku']
            cargotype = row['cargotype'].split(',') if row['cargotype'] else []
            if sku in cargotype_data:
                cargotype_data[sku].extend(cargotype)
            else:
                cargotype_data[sku] = cargotype

    for item in data:
        sku = item['sku']
        if sku in sku_data:
            item['a'] = sku_data[sku].get('a')
            item['b'] = sku_data[sku].get('b')
            item['c'] = sku_data[sku].get('c')
        
        if sku in cargotype_data:
            item['cargotype'] = list(map(int, cargotype_data[sku]))

    return data