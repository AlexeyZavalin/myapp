import json


def write_order_to_json(item, quantity, price, buyer, date):
    order = {
        'item': item,
        'quantity': quantity,
        'price': price,
        'buyer': buyer,
        'date': date
    }
    orders = []
    with open('data/json/orders.json') as json_file:
        str_ = json_file.read()
        data = json.loads(str_)
        orders += data['orders']
    orders.append(order)
    with open('data/json/orders.json', 'w') as json_file:
        json.dump({'orders': orders}, json_file, indent=4)


write_order_to_json('Product 1', 3, 500, 'buyer', '21-06-2019')
