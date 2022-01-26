import lxml
from bs4 import BeautifulSoup
import multiprocessing as mp


class IMDBTop250PageParser:
    """
    Parser to process the IMDB TOP 250 list page to get the rank, title, link, rating and number of votes
    for the specified number of top movies (specified number <= 250)
    """

    URL = 'https://www.imdb.com/chart/top'

    def __init__(self, top_selection_number: int):
        self.top_selection_number = top_selection_number

    @staticmethod
    def __transform_rank_str(rank_str: str) -> int:
        return int(rank_str.strip().replace('.', ''))

    @staticmethod
    def __transform_vote_str(vote_str: str) -> int:
        return int(vote_str.removesuffix(' user ratings')
                   .split(' based on ')[1]
                   .replace(',', ''))

    # Parse the rank, title, link, rating and number of votes for the specified number of
    # top movies from the IMDB TOP 250 list (specified number <= 250)
    def parse(self, top250_movies_page_text: str):

        soup = BeautifulSoup(top250_movies_page_text, 'lxml')

        title_column_a_tags = soup.select('td.titleColumn a')[:self.top_selection_number]
        ranks = [self.__transform_rank_str(tag.previous_sibling) for tag in title_column_a_tags]
        titles = [str(tag.text) for tag in title_column_a_tags]
        relative_links = [str(tag.attrs.get('href')) for tag in title_column_a_tags]

        poster_column_span_tags = soup.select('td.posterColumn span[name=ir]')[:self.top_selection_number]
        ratings = [float(tag.attrs.get('data-value')) for tag in poster_column_span_tags]

        rating_column_tags = soup.select('td.ratingColumn.imdbRating strong')[:self.top_selection_number]
        votes = [self.__transform_vote_str(tag.attrs.get('title')) for tag in rating_column_tags]

        return ranks, titles, relative_links, ratings, votes


class IMDBTitlePageParser:
    """
    Parser to process IMDB title pages to get number of Oscars for the movies displayed on the specified links.
    An IMDB title page is a page that displays the details of a single movie. E.g. https://www.imdb.com/title/tt0111161/
    """

    BASE_URL = 'https://www.imdb.com'

    # Parse the number of Oscars
    @staticmethod
    def parse_num_of_won_oscars_from_movie_page(movie_details_page_text: str) -> int:
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
    @staticmethod
    def parse_num_of_won_oscars_from_movie_pages(movie_details_page_texts: [str]) -> [int]:
        pool = mp.Pool(mp.cpu_count())
        num_of_oscars = pool.map(IMDBTitlePageParser.parse_num_of_won_oscars_from_movie_page, movie_details_page_texts)
        return num_of_oscars
