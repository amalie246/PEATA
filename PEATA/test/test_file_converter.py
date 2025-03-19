import pytest
from unittest.mock import patch, mock_open
import json
import csv
from file_converter import FileConverter

# Test for saving JSON to file
@patch("builtins.open", new_callable=mock_open)
@patch("os.path.join", return_value="mocked_path/data.json")
def test_save_json_to_file(mock_path_join, mock_file):
    data = {"name": "Test", "value": 42}
    
    FileConverter.save_json_to_file(data, "data.json")
    
    mock_file.assert_called_once_with("data.json", "w", encoding="utf-8")
    handle = mock_file()
    handle.write.assert_called_once_with(json.dumps(data, indent=4, ensure_ascii=False))


# Test for saving JSON to CSV
@patch("builtins.open", new_callable=mock_open)
@patch("os.path.join", return_value="mocked_path/data.csv")
def test_save_json_to_csv(mock_path_join, mock_file):
    data = [
        {"name": "Test1", "value": 42},
        {"name": "Test2", "value": 84},
    ]
    
    converter = FileConverter()
    converter.save_json_to_csv(data, "data.csv")

    mock_file.assert_called_once_with("data.csv", mode="w", newline="", encoding="utf-8")

    # Check CSV content
    handle = mock_file()
    csv_content = handle.write.call_args_list
    assert "name,value" in csv_content[0][0][0]   # Header row
    assert "Test1,42" in csv_content[1][0][0]     # First row
    assert "Test2,84" in csv_content[2][0][0]     # Second row


# Test for invalid data in CSV
def test_invalid_data_for_csv(capfd):
    converter = FileConverter()
    invalid_data = {"key": "value"}  # Not a list of dicts

    converter.save_json_to_csv(invalid_data, "invalid.csv")

    out, _ = capfd.readouterr()
    assert "Ingen gyldige data å lagre." in out


# Test for `save_any_json_data` with JSON format
@patch("PEATA.file_converter.FileConverter.save_json_to_file")
def test_save_any_json_data_as_json(mock_save_json):
    data = {"name": "Test", "value": 42}
    converter = FileConverter()

    converter.save_any_json_data(data, "output", "json")

    mock_save_json.assert_called_once_with(data, "output.json")


# Test for `save_any_json_data` with CSV format
@patch("PEATA.file_converter.FileConverter.save_json_to_csv")
def test_save_any_json_data_as_csv(mock_save_csv):
    data = [
        {"name": "Test1", "value": 42},
        {"name": "Test2", "value": 84},
    ]
    converter = FileConverter()

    converter.save_any_json_data(data, "output", "csv")

    mock_save_csv.assert_called_once_with(data, "output.csv")


# Test for invalid file format
def test_invalid_file_format(capfd):
    data = {"name": "Test", "value": 42}
    converter = FileConverter()

    converter.save_any_json_data(data, "output", "xml")

    out, _ = capfd.readouterr()
    assert "Ingen gyldige data å lagre." not in out

