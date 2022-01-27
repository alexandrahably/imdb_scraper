import requests
import concurrent.futures


def fetch_page_as_text(session: requests.Session, page_url: str) -> str:
    """
    Get the English translated text of the page at the received URL
    """
    headers = {'Accept-Language': 'en-US'}
    response = session.get(page_url, headers=headers)
    response.raise_for_status()
    return response.text


def fetch_pages_as_text(session: requests.Session, base_url: str, relative_paths: list[str]) -> list[str]:
    """
    Downloads multiple pages concurrently, and returns the downloaded pages as text.
    The order of urls & requests is stable.
    """
    arg_tuples = ((session, f'{base_url}{relative_path}') for relative_path in relative_paths)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(lambda arg_tuple: fetch_page_as_text(*arg_tuple), arg_tuples)
        return results
