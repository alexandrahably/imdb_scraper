import requests
import concurrent.futures


class WebpageDownloader:

    def __init__(self, session: requests.Session):
        self.session = session

    # Getting English translated text of the page at the received URL
    def fetch_page_as_text(self, page_url: str):
        headers = {'Accept-Language': 'en-US'}
        response = self.session.get(page_url, headers=headers)
        return response.text

    # Fetching pages concurrently to speed up the download
    def fetch_pages_as_text(self, base_url: str, relative_paths: [str]):
        urls = map(lambda path: f'{base_url}{path}', relative_paths)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(self.fetch_page_as_text, urls)
            return results
