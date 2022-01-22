import lxml
from bs4 import BeautifulSoup


class IMDBTop250PageParser:
    """
    Parser to process the IMDB TOP 250 list page to get the rank, title, link, rating and number of votes
    for the specified number of top movies (specified number <= 250)
    """

    URL = 'https://www.imdb.com/chart/top'

    def __init__(self, top_selection_number: int):
        self.top_selection_number = top_selection_number

    @staticmethod
    def _transform_rank_str(rank_str: str) -> int:
        return int(rank_str.strip().replace('.', ''))

    @staticmethod
    def _transform_vote_str(vote_str: str) -> int:
        return int(vote_str.removesuffix(' user ratings')
                   .split(' based on ')[1]
                   .replace(',', ''))

    # Parse the rank, title, link, rating and number of votes for the specified number of
    # top movies from the IMDB TOP 250 list (specified number <= 250)
    def parse(self, top250_movies_page_text: str):

        soup = BeautifulSoup(top250_movies_page_text, 'lxml')

        title_column_a_tags = soup.select('td.titleColumn a')[:self.top_selection_number]
        ranks = [self._transform_rank_str(tag.previous_sibling) for tag in title_column_a_tags]
        titles = [str(tag.text) for tag in title_column_a_tags]
        relative_links = [str(tag.attrs.get('href')) for tag in title_column_a_tags]

        poster_column_span_tags = soup.select('td.posterColumn span[name=ir]')[:self.top_selection_number]
        ratings = [float(tag.attrs.get('data-value')) for tag in poster_column_span_tags]

        rating_column_tags = soup.select('td.ratingColumn.imdbRating strong')[:self.top_selection_number]
        votes = [self._transform_vote_str(tag.attrs.get('title')) for tag in rating_column_tags]

        return ranks, titles, relative_links, ratings, votes
