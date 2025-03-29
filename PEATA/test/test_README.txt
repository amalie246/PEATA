For testing using spyder:
    !pytest folder/test_file.py
    
    e.g.
    !pytest test/test_file_converter.py

for testing a single function only:
    !pytest folder/test_file::function_name

    e.g.
    !pytest test/test_file_converter.py::test_save_json_to_file

In some tests, you will have FAIL on purpose!