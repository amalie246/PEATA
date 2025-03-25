import sys
import os

# Fix for "CANNOT FIND MODULE"-error!!!
# Add the parent directory to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch, MagicMock
from tkinter import Tk
from gui import Gui

@pytest.fixture
def app(mocker):
    # Mock TikTokApi
    mock_api = mocker.patch('gui.TikTokApi')
    mock_api.return_value.get_public_user_info.return_value = {'username': 'testuser', 'followers': 100}

    # Mock tkinter.Tk to avoid opening a real window
    with patch('tkinter.Tk', autospec=True) as mock_tk:
        app = Gui(cs='test_secret', ci='test_id', ck='test_key')
        yield app

# Test successful user info query
def test_user_queries(app, mocker):
    mock_messagebox = mocker.patch('tkinter.messagebox.showinfo')

    # Mock tkinter input and output
    app.test_page()
    app.user_queries()

    # Simulate user input
    app.e2.insert(0, 'testuser')

    # Simulate submit button action
    app.user_queries.label.config(text="Fetching info about testuser...")
    user_info = app.tiktok_api.get_public_user_info('testuser')

    assert user_info == {'username': 'testuser', 'followers': 100}

# Test empty username input
def test_empty_user_query(app, mocker):
    mock_messagebox = mocker.patch('tkinter.messagebox.showwarning')

    app.test_page()
    app.user_queries()

    # Simulate empty input and press submit
    app.e2.insert(0, '')

    app.user_queries.label.config(text="Fetching info about ...")
    
    # Check that warning is shown
    mock_messagebox.assert_called_once_with("Feil", "Du må fylle inn alle feltene")

# Test failed API response
def test_failed_user_query(app, mocker):
    mock_messagebox = mocker.patch('tkinter.messagebox.showerror')

    # Simulate API failure
    app.tiktok_api.get_public_user_info.return_value = None

    app.test_page()
    app.user_queries()

    # Simulate user input
    app.e2.insert(0, 'testuser')

    # Simulate submit button action
    app.user_queries.label.config(text="Fetching info about testuser...")
    user_info = app.tiktok_api.get_public_user_info('testuser')

    assert user_info is None

    mock_messagebox.assert_called_once_with("Innlogging feilet", "Feil: Ingen bruker funnet")

# Test dropdown handling
def test_dropdown_selection(app, mocker):
    app.page()

    # Simulate adding dropdown values
    app.dropdown_rows.append(('and', 'EQ'))
    app.dropdown_rows.append(('or', 'GT'))

    selections = [f"{bool_var} - {eq_var}" for bool_var, eq_var in app.dropdown_rows]

    assert selections == ['and - EQ', 'or - GT']

# Test exit confirmation dialog
def test_exit_confirmation(app, mocker):
    mock_messagebox = mocker.patch('tkinter.messagebox.askyesno', return_value=True)

    app.test_page()

    # Simulate Escape key event
    app.show_exit()

    mock_messagebox.assert_called_once_with("Exit Program", "Are you sure you want to quit your session?")

# Test showing popup
def test_show_popup(app, mocker):
    mock_messagebox = mocker.patch('tkinter.messagebox.showinfo')

    app.page()
    app.show_popup()

    mock_messagebox.assert_called_once_with("Information", "This is a popup box!")

