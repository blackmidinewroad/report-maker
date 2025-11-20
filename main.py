import argparse
import csv
import os
from collections import defaultdict

from tabulate import tabulate

REPORTS = {
    'performance': lambda data: calc_performance(data),
}


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Creates report from csv files and displayes it in terminal.')
    parser.add_argument(
        '--files',
        nargs='+',
        type=str,
        required=True,
        help='Specify csv files paths separated by spaces.',
    )
    parser.add_argument(
        '--report',
        choices=REPORTS.keys(),
        type=str,
        required=True,
        help=f'Specify the name of the report. Available reports: {", ".join(REPORTS.keys())}.',
    )

    return parser


def validate_args(parser: argparse.ArgumentParser, args: argparse.Namespace) -> None:
    for file_path in args.files:
        if not os.path.exists(file_path):
            parser.error(f"Path doesn't exist: {file_path}")

        _, ext = os.path.splitext(file_path)
        if ext.lower() != '.csv':
            parser.error(f"Incorrect file format ({ext}): {file_path}. All files should be in 'csv' format.")


def get_args(parser: argparse.ArgumentParser, inp_args: list[str] = None) -> argparse.Namespace:
    args = parser.parse_args(inp_args)
    validate_args(parser, args)

    return args


def load_employees_data(file_paths: list[str]) -> list[dict[str, str]]:
    employees_data = []

    for file_path in file_paths:
        with open(file_path, encoding='utf-8') as file:
            lines = csv.DictReader(file)
            employees_data.extend(lines)

    return employees_data


def calc_performance(employees_data: list[dict]) -> dict[str, float]:
    performance_by_pos = defaultdict(list)

    for employee in employees_data:
        performance_by_pos[employee['position']].append(float(employee['performance']))

    for position in performance_by_pos:
        performance_by_pos[position] = sum(performance_by_pos[position]) / len(performance_by_pos[position])

    return performance_by_pos


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

    employees_data = load_employees_data(args.files)
    report = REPORTS[args.report](employees_data)

    display_report(report, grouping_col_name='position', report_name=args.report)


if __name__ == "__main__":
    main()
