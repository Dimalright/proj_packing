import csv


def read_csv_file(file_path, sku_file_path, sku_cargotypes_file_path, orderkey):
    """
    Функция для чтения CSV-файла и фильтрации данных по ключу заказа.
    """
    items = []
    sku_set = set()

    with open(file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            if row.get('orderkey') == orderkey:
                sku = row['sku']
                if sku not in sku_set:
                    item = {
                        'selected_cartontype': row['selected_cartontype'],
                        'box_num': int(row['box_num']),
                        'recommended_cartontype': row['recommended_cartontype'],
                        'selected_carton': row['selected_carton'],
                        'sel_calc_cube': float(row['sel_calc_cube']),
                        'recommended_carton': row['recommended_carton'],
                        'pack_volume': float(row['pack_volume']),
                        'rec_calc_cube': float(row['rec_calc_cube']),
                        'goods_wght': float(row['goods_wght']) if row['goods_wght'] else None,
                        'sku': sku,
                        'barcode': None,
                        'name': None,
                        'pic': None,
                        'who': row['who'],
                        'trackingid': row['trackingid'],
                        'a': None,
                        'b': None,
                        'c': None,
                        'cargotype': [],
                    }
                    items.append(item)
                    sku_set.add(sku)

    order = {
        'orderId': orderkey,
        'items': items
    }

    sku_data = {}
    cargotype_data = {}
    barcode_data = {}

    with open(sku_file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sku = row['sku']
            if sku in sku_set:
                sku_data[sku] = {
                    'a': float(row['a']),
                    'b': float(row['b']),
                    'c': float(row['c']),
                    'name': row['name'],
                    'pic': row['pic']
                }

    with open(sku_cargotypes_file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sku = row['sku']
            cargotype = row['cargotype'].split(',') if row['cargotype'] else []
            if sku in sku_set:
                cargotype_data.setdefault(sku, []).extend(cargotype)

    with open(sku_file_path, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sku = row['sku']
            if sku in sku_set:
                barcode = int(row['barcode'])
                barcode_data[sku] = barcode

    for item in items:
        sku = item['sku']
        if sku in sku_data:
            item['a'] = sku_data[sku].get('a')
            item['b'] = sku_data[sku].get('b')
            item['c'] = sku_data[sku].get('c')
            item['name'] = sku_data[sku].get('name')
            item['pic'] = sku_data[sku].get('pic')

        if sku in cargotype_data:
            item['cargotype'] = list(map(int, cargotype_data[sku]))

        if sku in barcode_data:
            item['barcode'] = barcode_data[sku]

    return order
