import lxml
from bs4 import BeautifulSoup
import multiprocessing as mp


class IMDBTitlePageParser:
    """
    Parser to process IMDB title pages to get number of Oscars for the movies displayed on the specified links.
    An IMDB title page is a page that displays the details of a single movie. E.g. https://www.imdb.com/title/tt0111161/
    """

    BASE_URL = 'https://www.imdb.com'

    def __init__(self):
        pass

    # Parse the number of Oscars
    @staticmethod
    def _parse_num_of_won_oscars(movie_details_page_text: str) -> int:
        soup = BeautifulSoup(movie_details_page_text, 'lxml')
        # Find the awards section
        soup_query = 'section[cel_widget_id="StaticFeature_Awards"] a[class="ipc-metadata-list-item__label ipc-metadata-list-item__label--link"]'
        awards_tags = soup.select(soup_query)
        # Sometimes the awards section is totally missing
        if len(awards_tags) == 0:
            return 0
        # Parse the available awards text
        awards = awards_tags[0].text
        if awards is not None and "Won" in awards and "Oscar" in awards:
            oscars_count = int(awards.removeprefix("Won").removesuffix("s").removesuffix("Oscar").strip())
            return oscars_count
        else:
            return 0

    # Find the number of Oscars
    def parse_num_of_won_oscars_from_movie_page(self, movie_details_page_texts: [str]):
        pool = mp.Pool(mp.cpu_count())
        num_of_oscars = pool.map(self._parse_num_of_won_oscars, movie_details_page_texts)
        return num_of_oscars
