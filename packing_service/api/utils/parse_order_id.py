from csv import DictReader


def get_orderkey():
 
    orders_dict = DictReader(open("./data/data.csv", encoding='utf-8'))

    orderkey_dict = []

    for row in orders_dict:
        orderkey_dict.append(row['orderkey'])
    
    return orderkey_dict