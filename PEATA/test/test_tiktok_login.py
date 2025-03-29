import sys
import os

# Fix for "CANNOT FIND MODULE"-error!!!
# Add the parent directory to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from tkinter import Tk
from tiktokLogin import Login

@pytest.fixture
def app():
    root = Tk()
    app = Login(root)
    yield app
    root.destroy()

# Test successful login
@patch('login.requests.post')
def test_successful_login(mock_post, app, mocker):
    # Mock successful response from API
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    # Simulate filling out the form
    app.e2.insert(0, 'test_client_id')
    app.e3.insert(0, 'test_client_key')
    app.e4.insert(0, 'test_client_secret')

    # Mock messagebox and window destroy
    mock_showinfo = mocker.patch('tkinter.messagebox.showinfo')
    mock_destroy = mocker.patch.object(app.master, 'destroy')

    # Call the login function
    app.login()

    # Assertions
    mock_post.assert_called_once_with(
        "https://open.tiktokapis.com/v2/oauth/token/",
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        data={
            'client_id': 'test_client_id',
            'client_secret': 'test_client_secret',
            'client_key': 'test_client_key',
            'grant_type': 'client_credentials'
        }
    )
    mock_showinfo.assert_called_once_with("Innlogging vellykket", "Velkommen!")
    mock_destroy.assert_called_once()


# Test failed login due to invalid credentials
@patch('login.requests.post')
def test_failed_login(mock_post, app, mocker):
    # Mock failed response from API
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_response.text = "Invalid credentials"
    mock_post.return_value = mock_response

    # Simulate filling out the form
    app.e2.insert(0, 'test_client_id')
    app.e3.insert(0, 'test_client_key')
    app.e4.insert(0, 'wrong_secret')

    # Mock messagebox
    mock_showerror = mocker.patch('tkinter.messagebox.showerror')

    # Call the login function
    app.login()

    # Assertions
    mock_showerror.assert_called_once_with("Innlogging feilet", "Feil: 401 - Invalid credentials")


# Test empty input (should show warning)
def test_empty_fields(app, mocker):
    # Mock messagebox
    mock_showwarning = mocker.patch('tkinter.messagebox.showwarning')

    # Call login with empty fields
    app.login()

    # Assertions
    mock_showwarning.assert_called_once_with("Feil", "Du må fylle inn alle feltene")


# Test connection failure (network issue)
@patch('login.requests.post', side_effect=requests.exceptions.RequestException("Network Error"))
def test_connection_failure(mock_post, app, mocker):
    # Simulate filling out the form
    app.e2.insert(0, 'test_client_id')
    app.e3.insert(0, 'test_client_key')
    app.e4.insert(0, 'test_client_secret')

    # Mock messagebox
    mock_showerror = mocker.patch('tkinter.messagebox.showerror')

    # Call login function
    app.login()

    # Assertions
    mock_showerror.assert_called_once_with("Innlogging feilet", "Tilkoblingsfeil: Network Error")


# Test opening main window after successful login
@patch('login.requests.post')
def test_open_main_window(mock_post, app, mocker):
    # Mock successful response from API
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    # Simulate filling out the form
    app.e2.insert(0, 'test_client_id')
    app.e3.insert(0, 'test_client_key')
    app.e4.insert(0, 'test_client_secret')

    # Mock destroy and Toplevel
    mock_destroy = mocker.patch.object(app.master, 'destroy')
    mock_toplevel = mocker.patch('tkinter.Toplevel')

    # Call login function
    app.login()

    # Assertions
    mock_toplevel.assert_called_once()


# Test valid API connection
@patch('login.requests.post')
def test_test_connection_success(mock_post, app):
    # Mock successful response from API
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_post.return_value = mock_response

    success, message = app.test_connection('client_id', 'client_key', 'client_secret')

    assert success is True
    assert message == "API-tilkobling vellykket!"


# Test failed API connection (e.g., 403 error)
@patch('login.requests.post')
def test_test_connection_fail(mock_post, app):
    # Mock failed response from API
    mock_response = MagicMock()
    mock_response.status_code = 403
    mock_response.text = "Forbidden"
    mock_post.return_value = mock_response

    success, message = app.test_connection('client_id', 'client_key', 'client_secret')

    assert success is False
    assert message == "Feil: 403 - Forbidden"


# Test network error during API connection
@patch('login.requests.post', side_effect=requests.exceptions.RequestException("Connection Error"))
def test_test_connection_network_error(mock_post, app):
    success, message = app.test_connection('client_id', 'client_key', 'client_secret')

    assert success is False
    assert message == "Tilkoblingsfeil: Connection Error"

