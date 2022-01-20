import requests
import lxml
from bs4 import BeautifulSoup
import multiprocessing
from imdb_scraper import Movie


class IMDBScraper:
    IMDB_BASE_URL = 'http://www.imdb.com'
    IMDB_TOP250_MOVIES_URL = 'http://www.imdb.com/chart/top'

    def __init__(self, session: requests.Session, top_selection_number: int = 20):
        self.top_selection_number = top_selection_number
        self.session = session

    def __calculate_num_of_won_oscars(self, awards: str):
        if awards is not None and "Won" in awards:
            oscars_count = int(awards.removeprefix("Won").removesuffix("Oscars").removesuffix("Oscar").strip())
            return oscars_count
        else:
            return 0

    def __get_awards_from_link(self, movie_relative_link: str):
        movie_page_url = self.IMDB_BASE_URL + movie_relative_link
        movie_page_response = self.session.get(movie_page_url)
        soup = BeautifulSoup(movie_page_response.text, 'lxml')
        soup_query = 'section[cel_widget_id="StaticFeature_Awards"] a[class="ipc-metadata-list-item__label ipc-metadata-list-item__label--link"]'
        awards = soup.select(soup_query)[0].text
        return awards

    def scrape_top_movies(self):
        headers = {'Accept-Language': 'en-US'}
        # Downloading imdb top 250 movie's data
        # Getting English translated titles from the movies
        headers = {'Accept-Language': 'en-US'}
        response = self.session.get(self.IMDB_TOP250_MOVIES_URL, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')

        # Parse movie details
        ranks = [int(tag.previous_sibling.strip().replace('.', '')) for tag in soup.select('td.titleColumn a')]
        titles = [tag.text for tag in soup.select('td.titleColumn a')]
        years = [int(tag.text[1:-1]) for tag in soup.select('td.titleColumn span')]
        links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
        ratings = [float(b.attrs.get('data-value')) for b in soup.select('td.posterColumn span[name=ir]')]
        votes = [int(b.attrs.get('title').removesuffix(' user ratings').split(' based on ')[1].replace(',', ''))
                 for b in soup.select('td.ratingColumn.imdbRating strong')]

        movies_list = []

        for index in range(0, self.top_selection_number):
            # Downloading awards
            awards = self.__get_awards_from_link(links[index])
            num_of_won_oscars = self.__calculate_num_of_won_oscars(awards)

            data = Movie(rank=ranks[index],
                         title=titles[index],
                         year=years[index],
                         imdb_rating=ratings[index],
                         num_of_votes=votes[index],
                         num_of_won_oscars=num_of_won_oscars)
            movies_list.append(data)

        return movies_list
