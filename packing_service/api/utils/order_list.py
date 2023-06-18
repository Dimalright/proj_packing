import csv


def get_order_list(self, orderkey):
    """
    Получить список заказов, соответствующих указанному ключу заказа.
    """
    order_list = list(csv.reader(open(self.FILE_PATH)))
    return [el for el in order_list[1:] if el[2] == orderkey]