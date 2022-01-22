from .imdb_top250_page_parser import IMDBTop250PageParser
from .imdb_title_page_parser import IMDBTitlePageParser
from .movie import Movie
from .webpage_downloader import WebpageDownloader


class IMDBTop20Scraper:
    """
    For scraping the top 20 movies from IMDB
    """

    TOP_SELECTION_NUMBER = 20  # The top250 page can return max 250 movies from the top.

    def __init__(self, page_downloader: WebpageDownloader,
                 top250_page_parser: IMDBTop250PageParser = IMDBTop250PageParser(TOP_SELECTION_NUMBER),
                 title_page_parser: IMDBTitlePageParser = IMDBTitlePageParser()):
        self.page_downloader = page_downloader
        self.top250_page_parser = top250_page_parser
        self.title_page_parser = title_page_parser

    def scrape(self):
        # Downloading movie main info
        top250_page_text = self.page_downloader.fetch_page_as_text(IMDBTop250PageParser.URL)
        ranks, titles, relative_links, ratings, votes = self.top250_page_parser.parse(top250_page_text)

        # Downloading number of Oscars
        movie_pages = self.page_downloader.fetch_pages_as_text(IMDBTitlePageParser.BASE_URL, relative_links)
        oscars = self.title_page_parser.parse_num_of_won_oscars_from_movie_page(movie_pages)

        movies = [Movie(rank=ranks[index],
                        title=titles[index],
                        imdb_rating=ratings[index],
                        num_of_votes=votes[index],
                        num_of_won_oscars=oscars[index])
                  for index in range(len(ranks))]

        return movies
