import argparse
from unittest.mock import patch

import pytest

import main


def test_args_multiple_files(session_parser, csv_file_paths):
    args = main.get_args(session_parser, ['--files', *csv_file_paths, '--report', 'performance'])

    assert args.report == 'performance'
    assert args.files == csv_file_paths


def test_args_one_files(session_parser, csv_file_paths):
    args = main.get_args(session_parser, ['--files', csv_file_paths[0], '--report', 'performance'])

    assert args.report == 'performance'
    assert len(args.files) == 1
    assert args.files[0] == csv_file_paths[0]


def test_args_no_files(capsys, session_parser):
    with pytest.raises(SystemExit):
        main.get_args(session_parser, ['--report', 'performance'])
    assert 'the following arguments are required: --files' in capsys.readouterr().err


def test_args_no_report(capsys, session_parser, csv_file_paths):
    with pytest.raises(SystemExit):
        main.get_args(session_parser, ['--files', *csv_file_paths])
    assert 'the following arguments are required: --report' in capsys.readouterr().err


def test_no_args(capsys, session_parser):
    with pytest.raises(SystemExit):
        main.get_args(session_parser, [])
    assert 'the following arguments are required: --files, --report' in capsys.readouterr().err


def test_args_invalid_report_value(capsys, session_parser, csv_file_paths):
    with pytest.raises(SystemExit):
        main.get_args(session_parser, ['--files', *csv_file_paths, '--report', 'some_report'])
    assert "invalid choice: 'some_report'" in capsys.readouterr().err


def test_valid_multiple_files(session_parser, csv_file_paths):
    main.validate_args(session_parser, argparse.Namespace(files=csv_file_paths))


def test_valid_one_file(session_parser, csv_file_paths):
    main.validate_args(session_parser, argparse.Namespace(files=[csv_file_paths[0]]))


def test_file_doesnt_exist(capsys, session_parser, csv_file_paths, session_temp_dir):
    file_paths = csv_file_paths + [str(session_temp_dir / 'some_file.csv')]
    with pytest.raises(SystemExit):
        main.validate_args(session_parser, argparse.Namespace(files=file_paths))
    assert "Path doesn't exist" in capsys.readouterr().err


def test_incorrect_file_format(capsys, session_parser, csv_file_paths, json_file_path):
    file_paths = csv_file_paths + [json_file_path]
    with pytest.raises(SystemExit):
        main.validate_args(session_parser, argparse.Namespace(files=file_paths))
    assert 'Incorrect file format (.json)' in capsys.readouterr().err


def test_load_employees_data_one_file(csv_file_paths):
    data = main.load_employees_data([csv_file_paths[0]])

    assert len(data) == 9
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    assert data[0]['name'] == 'David Chen'
    assert data[0]['position'] == 'Mobile Developer'
    assert data[0]['performance'] == '4.6'


def test_load_employees_data_multiple_files(csv_file_paths):
    data = main.load_employees_data(csv_file_paths)

    assert len(data) == 15
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    assert data[-1]['name'] == 'Sarah Johnson'
    assert data[-1]['position'] == 'Fullstack Developer'
    assert data[-1]['performance'] == '4.7'


def test_calc_performance(csv_file_paths):
    employees_data = main.load_employees_data(csv_file_paths)
    result = main.calc_performance(employees_data)

    expected = {
        'Backend Developer': 4.83,
        'DevOps Engineer': 4.8,
        'Data Engineer': 4.7,
        'Fullstack Developer': 4.7,
        'Frontend Developer': 4.65,
        'Data Scientist': 4.65,
        'Mobile Developer': 4.6,
        'QA Engineer': 4.5,
    }

    assert len(result) == 8
    assert isinstance(result, dict)

    for pos in expected:
        assert pos in result
        assert abs(expected[pos] - result[pos]) < 0.01


@pytest.mark.parametrize(
    'is_sorted, is_reverse_sort, expected_order',
    [
        pytest.param(True, True, ['Backend Developer', 'Data Engineer', 'Mobile Developer'], id='sorted_desc'),
        pytest.param(True, False, ['Mobile Developer', 'Data Engineer', 'Backend Developer'], id='sorted_asc'),
        pytest.param(False, False, ['Backend Developer', 'Mobile Developer', 'Data Engineer'], id='unsorted'),
    ],
)
def test_display_report(is_sorted, is_reverse_sort, expected_order):
    test_data = {
        'Backend Developer': 4.83,
        'Mobile Developer': 4.6,
        'Data Engineer': 4.7,
    }

    grouping_col_name = 'position'
    report_name = 'performance'

    with patch('main.tabulate') as mock_tabulate:
        main.display_report(
            report=test_data,
            grouping_col_name=grouping_col_name,
            report_name=report_name,
            is_sorted=is_sorted,
            is_reverse_sort=is_reverse_sort,
        )

        expected_table = [(i, pos, f'{test_data[pos]:.2f}') for i, pos in enumerate(expected_order, 1)]

        mock_tabulate.assert_called_once_with(expected_table, headers=['', grouping_col_name, report_name], disable_numparse=True)
