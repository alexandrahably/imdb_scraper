import requests
import lxml
from bs4 import BeautifulSoup


class WebpageDownloader:

    def __init__(self, session: requests.Session):
        self.session = session

    # Getting English translated text of the page at the received URL
    def get_english_page_as_text(self, page_url: str):
        headers = {'Accept-Language': 'en-US'}
        response = self.session.get(page_url, headers=headers)
        return response.text

    def get_english_pages_as_text(self, page_urls: [str]):
        pages = []
        for link in page_urls:
            response_text = self.get_english_page_as_text(link)
            pages.append(response_text)
        return pages
