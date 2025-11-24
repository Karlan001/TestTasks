import argparse
import csv
from tabulate import tabulate

parser = argparse.ArgumentParser()

parser.add_argument('--files', type=str, nargs="+", help='Необходимо указать имя файла')
parser.add_argument('--report', type=str, help='Необходимо указать имя будущего отчета')

args = parser.parse_args()
print(args)


def get_data_from_file(file_path: str) -> list:
    data = list()
    with open(file_path, 'r', encoding='utf-8') as read_file:
        reader = csv.DictReader(read_file)
        for i in reader:
            data.append(i)
    return data


def prepare_dataset(list_data: list) -> tuple:
    if list_data:
        headers = [title for title in list_data[0].keys() if title == 'name' or title == 'performance']
        print(headers)
        body = list()
        for data in list_data:
            a = [v for k, v in data.items() if k == 'name' or k == 'performance']
            body.append(a)
        body.sort(key=lambda empl: empl[1], reverse=True)
        return headers, body


def create_report(report_name: str, headers: list, body: list) -> None:
    dataset = dict()
    for head in headers:
        dataset[head] = []
    for i in body:
        dataset["name"].append(i[0])
        dataset["performance"].append(i[1])
    with open(f'{report_name}.csv', 'w', encoding='utf-8') as write_file:
        writer = csv.DictWriter(write_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(dataset)


def print_console(headers: list, body: list) -> None:
    print(tabulate(body, headers=headers))


data = get_data_from_file(args.files[0])
headers, body = prepare_dataset(data)
print_console(headers, body)
create_report(args.report, headers, body)
# data = [
#     ["Alice", 30, "New York"],
#     ["Bob", 24, "London"],
#     ["Charlie", 35, "Paris"]
# ]
# headers = ["Name", "Age", "City"]
#
# print(tabulate(data, headers=headers))
