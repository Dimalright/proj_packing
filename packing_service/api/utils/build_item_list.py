def build_items_list(self, sku, count_weight_dict, sku_info_dict):
    """
    Строит список товаров для упаковки.
    """
    items_list = []
    sku_set = set()

    for el in sku:
        if el not in sku_set:
            temp_dict = sku_info_dict[el].copy()
            temp_dict['sku'] = el
            temp_dict['count'] = count_weight_dict[el]['count']
            temp_dict['weight'] = count_weight_dict[el]['weight']
            items_list.append(temp_dict)
            sku_set.add(el)

    return items_list
