import csv


def get_order_by_id(order_id):
    """
    Получает информацию о заказе по его идентификатору.
    """
    with open('data/data.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['orderkey'] == order_id:
                return row
        return None

def cancel_order(order_id):
    """
    Отменяет заказ по его идентификатору.
    """
    orders = []
    with open('data/data.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            orders.append(row)

    for order in orders:
        if order['orderkey'] == order_id:
            order['status'] = 'Canceled'

    with open('data/data.csv', 'w', newline='') as file:
        fieldnames = orders[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(orders)
