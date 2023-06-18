def build_order_after_ml(self, orderkey, data, count_weight_dict, sku_info_dict, sku_info_dict2):
    """
    Строит структуру заказа после применения машинного обучения.
    """
    order_after_ml = {
            'orderId': orderkey,
            'packages': []
        }

    package_id = 1

    sku_counts = {}
    for package_data in data.get('package', []):
        for sku, recommended_packs in package_data.items():
            count = count_weight_dict[sku]['count']
            if sku in sku_counts:
                if count > sku_counts[sku]['count']:
                    sku_counts[sku] = {
                        'count': count,
                        'package': package_data,
                    }
            else:
                sku_counts[sku] = {
                    'count': count,
                    'package': package_data,
                }

    for sku, package_data in sku_counts.items():
        package = {
            'packageId': package_id,
            'recommendedPacks': package_data['package'][sku],
            'items': []
        }

        item = sku_info_dict[sku].copy()
        item.update(sku_info_dict2[sku])
        item['sku'] = sku
        item['count'] = package_data['count']
        item['weight'] = count_weight_dict[sku]['weight']
        package['items'].append(item)

        order_after_ml['packages'].append(package)

        package_id += 1

        return order_after_ml
