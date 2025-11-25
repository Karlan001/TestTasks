import argparse
import csv
from tabulate import tabulate
from datetime import datetime
from pathlib import Path

parser = argparse.ArgumentParser()

parser.add_argument(
    "--files",
    type=str,
    nargs="+",
    help="Необходимо указать относительный или абсолютный путь до файла",
)
parser.add_argument("--report", type=str, help="Необходимо указать имя будущего отчета", default='report')


def get_data_from_file(file_path: str) -> list:
    data = list()
    try:
        with open(file_path, "r", encoding="utf-8") as read_file:
            reader = csv.DictReader(read_file)
            for i in reader:
                data.append(i)
        return data
    except FileNotFoundError:
        print(f'Файл по указанному пути {file_path} не найден')


def prepare_dataset(list_data: list) -> tuple:
    if list_data:
        headers = [
            title
            for title in list_data[0].keys()
            if title == "name" or title == "performance"
        ]
        body = list()
        for data in list_data:
            a = [v for k, v in data.items() if k == "name" or k == "performance"]
            body.append(a)
        return headers, body
    print("Передан пустой файл")


def print_console(headers: list, body: list) -> None:
    print(tabulate(body, headers=headers))


def create_report(report_name: str, headers: list, body: list) -> None:
    data = [dict((k, v) for k, v in zip(headers, val)) for val in body]
    sorted_data = sorted(data, key=lambda x: x["performance"], reverse=True)
    new_report_name = f'{report_name}.csv' if not Path(f'{report_name}.csv').exists() else f'{report_name}-{datetime.now()}.csv'
    print_console(headers, [i.values() for i in sorted_data])
    with open(new_report_name, "w", encoding="utf-8") as write_file:
        writer = csv.DictWriter(write_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(sorted_data)


def main():
    if args.files:
        for file in args.files:
            data = get_data_from_file(file)
            try:
                headers, body = prepare_dataset(data)
                create_report(args.report, headers, body)
            except TypeError:
                continue
    else:
        print("Вы не передали ни одно пути до файла")


if __name__ == '__main__':
    args = parser.parse_args()
    main()
