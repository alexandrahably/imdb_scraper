import pytest
import unittest
from unittest import mock
from requests.exceptions import HTTPError

from src.imdb.webpage_downloader import fetch_page_as_text, fetch_pages_as_text


def mock_session_response(status=200, content="CONTENT", text_data=None, raise_for_status=None):
    mock_resp = mock.MagicMock()
    type(mock_resp.return_value).status_code = mock.PropertyMock(return_value=status)
    type(mock_resp.return_value).content = content

    mock_resp.return_value.raise_for_status = mock.MagicMock()
    if raise_for_status:
        mock_resp.return_value.raise_for_status.side_effect = raise_for_status
    if text_data:
        type(mock_resp.return_value).text = mock.PropertyMock(return_value=text_data)
    session_return_value = mock.MagicMock(get=mock_resp)
    return session_return_value


class TestWebpageDownloader(unittest.TestCase):

    @mock.patch('src.imdb.webpage_downloader.requests.session', autospec=True)
    def test_fetch_page_as_text_when_IMDB_is_up(self, session_mock):
        session_mock.return_value = mock_session_response(text_data="hey")

        response = fetch_page_as_text(session_mock(),"test url")
        session_mock.return_value.get.assert_called_once_with('test url', headers={'Accept-Language': 'en-US'})
        self.assertEqual(response, 'hey', 'Response was successfully returned.')
        self.assertEqual(session_mock.return_value.get.called, True, "Session get was called")
        self.assertEqual(session_mock.return_value.get.return_value.raise_for_status.called, True,
                         "Raise for status was called")

    @mock.patch('src.imdb.webpage_downloader.requests.session', autospec=True)
    def test_fetch_page_as_text_when_IMDB_is_down(self, session_mock):
        session_mock.return_value = mock_session_response(status=500, raise_for_status=HTTPError("IMDB is down"))
        self.assertRaises(HTTPError, fetch_page_as_text, session_mock(), "test url")
