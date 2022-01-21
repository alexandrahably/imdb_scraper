import lxml
from bs4 import BeautifulSoup


class IMDBPageParser:

    def __init__(self, top_selection_number: int):
        self.top_selection_number = top_selection_number

    def __parse_ranks_titles_and_links(self, top_250_page_soup: BeautifulSoup):
        title_column_a_tags = top_250_page_soup.select('td.titleColumn a')[:self.top_selection_number]
        ranks = [int(tag.previous_sibling.strip().replace('.', '')) for tag in title_column_a_tags]
        titles = [tag.text for tag in title_column_a_tags]
        links = [a.attrs.get('href') for a in title_column_a_tags]
        return ranks, titles, links

    def __parse_ratings(self, top_250_page_soup: BeautifulSoup):
        poster_column_span_tags = top_250_page_soup.select('td.posterColumn span[name=ir]')[:self.top_selection_number]
        ratings = [float(b.attrs.get('data-value')) for b in poster_column_span_tags]
        return ratings

    def __parse_votes(self, top_250_page_soup: BeautifulSoup):
        rating_column_tags = top_250_page_soup.select('td.ratingColumn.imdbRating strong')[
                                    :self.top_selection_number]
        votes = [int(b.attrs.get('title').removesuffix(' user ratings').split(' based on ')[1].replace(',', ''))
                 for b in rating_column_tags]
        return votes

    # Parse the rank, title, link, rating and number of votes for the specified number of
    # top movies from the IMDB TOP 250 list (specified number <= 250)
    def parse_top_movies_main_info(self, top250_movies_page_text: str):
        soup = BeautifulSoup(top250_movies_page_text, 'lxml')
        ranks, titles, links = self.__parse_ranks_titles_and_links(soup)
        ratings = self.__parse_ratings(soup)
        votes = self.__parse_votes(soup)
        return ranks, titles, links, ratings, votes

    # Parse the number of Oscars from the IMDB movie page
    def parse_num_of_won_oscars(self, movie_details_page_text: str):
        soup = BeautifulSoup(movie_details_page_text, 'lxml')
        # Find the awards section
        soup_query = 'section[cel_widget_id="StaticFeature_Awards"] a[class="ipc-metadata-list-item__label ipc-metadata-list-item__label--link"]'
        awards_tags = soup.select(soup_query)
        if len(awards_tags) == 0:
            return 0
        awards = awards_tags[0].text
        # Parse awards text
        if awards is not None and "Won" in awards and "Oscar" in awards:
            oscars_count = int(awards.removeprefix("Won").removesuffix("Oscars").removesuffix("Oscar").strip())
            return oscars_count
        else:
            return 0