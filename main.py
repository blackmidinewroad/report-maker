import argparse
import csv
import os
from collections import defaultdict

from tabulate import tabulate


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Creates report from csv files and displayes it in terminal.')
    parser.add_argument(
        '--file',
        nargs='+',
        type=str,
        required=True,
        help='Specify csv files paths separated by spaces.',
    )
    parser.add_argument(
        '--report',
        type=str,
        required=True,
        help='Specify the name of the report.',
    )

    return parser


def validate_args(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    for file_path in args.file:
        if not os.path.exists(file_path):
            raise parser.error(f"Path doesn't exist: {file_path}")

        _, ext = os.path.splitext(file_path)
        if ext.lower() != '.csv':
            raise parser.error(f"Incorrect file format ({ext}): {file_path}. All files should be in 'csv' format.")


def get_args(parser: argparse.ArgumentParser) -> argparse.Namespace:
    args = parser.parse_args()
    validate_args(parser, args)

    return args


def get_data_from_files(file_paths: list[str]) -> list[dict]:
    data = []

    for file_path in file_paths:
        with open(file_path, encoding='utf-8') as file:
            lines = csv.DictReader(file)
            data.extend(lines)

    return data


def calc_perfomance(employees_data: list) -> dict[float]:
    perfomance = defaultdict(lambda: defaultdict(int))

    for employee_data in employees_data:
        perfomance[employee_data['position']]['performance_sum'] += float(employee_data['performance'])
        perfomance[employee_data['position']]['cnt'] += 1

    for position in perfomance:
        perfomance[position] = perfomance[position]['performance_sum'] / perfomance[position]['cnt']

    return perfomance


def display_report(report: dict, grouping_col_name: str, report_name: str, is_sorted: bool = True, is_reverse_sort: bool = True) -> None:
    headers = ['', grouping_col_name, report_name]
    if is_sorted:
        table = [
            (i, group_col, f'{res:.2f}')
            for i, (group_col, res) in enumerate(sorted(report.items(), key=lambda x: x[1], reverse=is_reverse_sort), 1)
        ]
    else:
        table = [(i, group_col, f'{res:.2f}') for i, (group_col, res) in enumerate(report.items(), 1)]

    print(tabulate(table, headers=headers, disable_numparse=True))


def main():
    parser = create_parser()
    args = get_args(parser)

    employees_data = get_data_from_files(args.file)
    perfomance = calc_perfomance(employees_data)

    display_report(report=perfomance, grouping_col_name='position', report_name=args.report)


if __name__ == "__main__":
    main()
