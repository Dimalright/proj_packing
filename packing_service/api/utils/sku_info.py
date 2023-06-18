import csv


def get_sku_info_dict(self):
    """
    Получить словари с информацией о товарных позициях (SKU).
    """
    sku_list = list(csv.reader(open(self.SKU_FILE_PATH)))
    cargotypes = list(csv.reader(open(self.SKU_CARGOTYPES_FILE_PATH)))

    sku_info_dict = {}
    sku_info_dict2 = {}

    for row in sku_list[1:]:
        sku_info_dict[row[1]] = {
            'size1': row[2],
            'size2': row[3],
            'size3': row[4],
            'type': []
        }
        sku_info_dict2[row[1]] = {
            'name': row[6],
            'pic': row[7],
            'barcode': row[5]
        }
    for row in cargotypes[1:]:
        if row[1] in sku_info_dict:
            sku_info_dict[row[1]].setdefault('type', []).append(row[2])

    return sku_info_dict, sku_info_dict2