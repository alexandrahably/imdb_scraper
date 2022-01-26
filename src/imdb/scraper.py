import requests

from src.imdb.parsers import IMDBTop250PageParser, IMDBTitlePageParser
from src.imdb.movie import Movie
from src.imdb.webpage_downloader import fetch_page_as_text, fetch_pages_as_text


class IMDBTop20Scraper:
    """
    For scraping the top 20 movies from IMDB
    """

    TOP_SELECTION_NUMBER = 20  # The top250 page can return max 250 movies from the top.

    def __init__(self,
                 top250_page_parser: IMDBTop250PageParser = IMDBTop250PageParser(TOP_SELECTION_NUMBER),
                 title_page_parser: IMDBTitlePageParser = IMDBTitlePageParser()):
        self.top250_page_parser = top250_page_parser
        self.title_page_parser = title_page_parser

    def __enter__(self):
        self.session = requests.session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def scrape(self) -> [Movie]:

        # Downloading movie main info
        top250_page_text = fetch_page_as_text(self.session, IMDBTop250PageParser.URL)
        ranks, titles, relative_links, ratings, votes = self.top250_page_parser.parse(top250_page_text)

        # Downloading number of Oscars
        movie_pages = fetch_pages_as_text(self.session, IMDBTitlePageParser.BASE_URL, relative_links)
        oscars = self.title_page_parser.parse_num_of_won_oscars_from_movie_pages(movie_pages)

        movies = [Movie(rank=ranks[index],
                        title=titles[index],
                        imdb_rating=ratings[index],
                        num_of_votes=votes[index],
                        num_of_won_oscars=oscars[index])
                  for index in range(len(ranks))]

        return movies
