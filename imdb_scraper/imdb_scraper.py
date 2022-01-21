from imdb_scraper.imdb_page_parser import IMDBPageParser
from imdb_scraper.movie import Movie
from imdb_scraper.webpage_downloader import WebpageDownloader


class IMDBTop20Scraper:
    IMDB_BASE_URL = 'http://www.imdb.com'
    IMDB_TOP250_MOVIES_URL = 'http://www.imdb.com/chart/top'  # Displays the top 250 movies
    TOP_SELECTION_NUMBER = 20  # The currently specified URL can handle max 250 movies from the top

    def __init__(self, page_downloader: WebpageDownloader,
                 page_parser: IMDBPageParser = IMDBPageParser(TOP_SELECTION_NUMBER)):
        self.page_downloader = page_downloader
        self.page_parser = page_parser

    def scrape_top_movies(self):
        # Downloading movie main info
        top250_page_text = self.page_downloader.get_english_page_as_text(self.IMDB_TOP250_MOVIES_URL)
        ranks, titles, links, ratings, votes = self.page_parser.parse_top_movies_main_info(top250_page_text)

        # Downloading number of Oscars from movie detail page
        awards_page_urls = map(lambda movie_relative_link: self.IMDB_BASE_URL + movie_relative_link, links)
        awards_pages = self.page_downloader.get_english_pages_as_text(awards_page_urls)
        oscars = list(map(self.page_parser.parse_num_of_won_oscars, awards_pages))

        movies_list = []
        for index in range(len(ranks)):
            movie = Movie(rank=ranks[index],
                          title=titles[index],
                          imdb_rating=ratings[index],
                          num_of_votes=votes[index],
                          num_of_won_oscars=oscars[index])
            movies_list.append(movie)

        return movies_list
