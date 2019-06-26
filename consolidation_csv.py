import os
import csv
import re


def transpose(array):
    """:return Транспонированная матрица"""
    return list(zip(*array))


def write_to_csv(path_to_file):
    data = get_data('data/txt')
    with open(path_to_file, 'w', newline='', encoding='utf-8') as csv_file:
        headers = data.pop(0)
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        data = transpose(data)
        for row in data:
            new_row = {headers[0]: row[0], headers[1]: row[1], headers[2]: row[2], headers[3]: row[3]}
            writer.writerow(new_row)


def get_data(path_to_directory):
    """ :return Список параметров системы """
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']

    for address, dirs, files in os.walk(path_to_directory):
        for file in files:
            with open(f'{path_to_directory}/{file}', 'r', encoding='windows-1251') as txt_file:
                for row in txt_file:
                    brand = re.match(r'Изготовитель системы:\s+(.+)', row)
                    if brand is not None:
                        os_prod_list.append(brand.group(1))
                    name = re.match(r'Название ОС:\s+(.+)', row)
                    if name is not None:
                        os_name_list.append(name.group(1))
                    code = re.match(r'Код продукта:\s+(.+)', row)
                    if code is not None:
                        os_code_list.append(code.group(1))
                    type_ = re.match(r'Тип системы:\s+(.+)', row)
                    if type_ is not None:
                        os_type_list.append(type_.group(1))
    main_data = [headers, os_prod_list, os_name_list, os_code_list, os_type_list]
    return main_data


write_to_csv('data/result.csv')
