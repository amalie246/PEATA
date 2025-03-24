import sys
import os

# Fix for "CANNOT FIND MODULE"-error!!!
# Add the parent directory to PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# pip install pytest mock-api, this uses internet connection
from unittest.mock import patch, MagicMock
from api import TikTokApi

# Mock environment variables
@patch.dict('os.environ', {'CLIENT_KEY': 'test_key', 'CLIENT_SECRET': 'test_secret'})
def test_obtain_access_token(mocker):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'access_token': 'test_token'}

    mocker.patch('requests.post', return_value=mock_response)

    api = TikTokApi()
    assert api.access_token == 'test_token'


@patch.dict('os.environ', {'CLIENT_KEY': 'test_key', 'CLIENT_SECRET': 'test_secret'})
def test_get_videos(mocker):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'data': {
            'videos': [{'id': 1, 'description': 'Test video'}],
            'has_more': False
        }
    }

    mocker.patch('requests.post', return_value=mock_response)

    api = TikTokApi()
    videos = api.get_videos('testuser', 'testkeyword', '2025-01-01', '2025-01-10')

    assert len(videos) == 1
    assert videos[0]['id'] == 1
    assert videos[0]['description'] == 'Test video'


@patch.dict('os.environ', {'CLIENT_KEY': 'test_key', 'CLIENT_SECRET': 'test_secret'})
def test_get_video_comments(mocker):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'data': {
            'comments': [{'id': 1, 'text': 'Nice video'}],
            'has_more': False
        }
    }

    mocker.patch('requests.post', return_value=mock_response)

    api = TikTokApi()
    comments = api.get_video_comments('12345')

    assert len(comments) == 1
    assert comments[0]['id'] == 1
    assert comments[0]['text'] == 'Nice video'


@patch.dict('os.environ', {'CLIENT_KEY': 'test_key', 'CLIENT_SECRET': 'test_secret'})
def test_get_public_user_info(mocker):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'display_name': 'Test User',
        'follower_count': 1000
    }

    mocker.patch('requests.post', return_value=mock_response)

    api = TikTokApi()
    user_info = api.get_public_user_info('testuser')

    assert user_info['display_name'] == 'Test User'
    assert user_info['follower_count'] == 1000


@patch.dict('os.environ', {'CLIENT_KEY': 'test_key', 'CLIENT_SECRET': 'test_secret'})
def test_get_music_info(mocker):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        'data': {
            'music': [{
                'id': '123',
                'title': 'Test Music',
                'author_name': 'Artist'
            }]
        }
    }

    mocker.patch('requests.post', return_value=mock_response)

    api = TikTokApi()
    music_info = api.get_music_info('123')

    assert music_info is not None
    assert music_info['id'] == '123'
    assert music_info['title'] == 'Test Music'
    assert music_info['author_name'] == 'Artist'