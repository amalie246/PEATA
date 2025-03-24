import sys
import os

# Fix for "CANNOT FIND MODULE"-error!!!
# Add the parent directory to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# pip install pytest pytest-mock pandas reportlab xlsxwriter
import pytest
from unittest.mock import patch, mock_open, MagicMock
import pandas as pd
from pathlib import Path
from fileHandler import FileHandler

# Mock configuration paths
@pytest.fixture(autouse=True)
def mock_config(mocker):
    mocker.patch('PEATA.config.CSV_FOLDER', 'mock_csv_folder')
    mocker.patch('PEATA.config.EXPORTS_FOLDER', 'mock_exports_folder')


# Test for getting the latest CSV file
@patch('pathlib.Path.glob')
@patch('os.path.getmtime')
def test_get_latest_csv_file(mock_getmtime, mock_glob, mocker):
    mock_file = MagicMock()
    mock_file.stem = "test_file"
    mock_glob.return_value = [mock_file]
    mock_getmtime.return_value = 1000

    handler = FileHandler()
    
    assert handler.file_path == mock_file
    mock_glob.assert_called_once_with('*.csv')
    mock_getmtime.assert_called_once()


# Test for opening a CSV file successfully
@patch('pandas.read_csv')
def test_open_file(mock_read_csv, mocker):
    mock_data = pd.DataFrame({"name": ["Test"], "value": [42]})
    mock_read_csv.return_value = mock_data

    handler = FileHandler()
    handler.file_path = "mock_csv_folder/test.csv"
    
    result = handler.open_file()

    mock_read_csv.assert_called_once_with("mock_csv_folder/test.csv")
    assert result.equals(mock_data)


# Test for file not found error
@patch('pandas.read_csv', side_effect=FileNotFoundError)
def test_open_file_not_found(mock_read_csv, capfd):
    handler = FileHandler()
    handler.file_path = "mock_csv_folder/test.csv"
    
    result = handler.open_file()
    out, _ = capfd.readouterr()

    assert "Error: The file mock_csv_folder/test.csv was not found." in out
    assert result is None


# Test for successful CSV export
@patch('builtins.open', new_callable=mock_open)
@patch('pandas.DataFrame.to_excel')
def test_export_as_excel(mock_to_excel, mock_file, mocker):
    mock_data = pd.DataFrame({"name": ["Test"], "value": [42]})
    handler = FileHandler()
    handler.data = mock_data
    handler.file_path = Path("mock_csv_folder/test.csv")

    handler.export_as_excel()

    mock_to_excel.assert_called_once()
    out_file = Path('mock_exports_folder/test.xlsx')
    assert out_file.name == "test.xlsx"


# Test for empty data export (Excel)
def test_export_as_excel_no_data(capfd):
    handler = FileHandler()
    handler.export_as_excel()

    out, _ = capfd.readouterr()
    assert "No data available to export." in out


# Test for successful PDF export
@patch('reportlab.pdfgen.canvas.Canvas')
def test_export_as_pdf(mock_canvas, mocker):
    mock_data = pd.DataFrame({"name": ["Test"], "value": [42]})
    handler = FileHandler()
    handler.data = mock_data
    handler.file_path = Path("mock_csv_folder/test.csv")

    handler.export_as_pdf()

    mock_canvas.assert_called_once()
    out_file = Path('mock_exports_folder/test.pdf')
    assert out_file.name == "test.pdf"


# Test for empty data export (PDF)
def test_export_as_pdf_no_data(capfd):
    handler = FileHandler()
    handler.export_as_pdf()

    out, _ = capfd.readouterr()
    assert "No data available to export." in out


# Test for closing the file
def test_close_file(capfd):
    handler = FileHandler()
    handler.data = pd.DataFrame({"name": ["Test"], "value": [42]})

    handler.close_file()

    out, _ = capfd.readouterr()
    assert "File data has been cleared from memory." in out
    assert handler.data is None


# Test for closing file when no file is open
def test_close_file_no_data(capfd):
    handler = FileHandler()
    handler.data = None

    handler.close_file()

    out, _ = capfd.readouterr()
    assert "No file data to close." in out


# Test for file opening error (e.g., permission error)
@patch('pandas.read_csv', side_effect=PermissionError("Permission denied"))
def test_open_file_permission_error(mock_read_csv, capfd):
    handler = FileHandler()
    handler.file_path = "mock_csv_folder/test.csv"
    
    result = handler.open_file()
    out, _ = capfd.readouterr()

    assert "Error opening file mock_csv_folder/test.csv: Permission denied" in out
    assert result is None
