import pytest
import unittest
from unittest import mock, TestCase

from src.imdb.scraper import IMDBTop20Scraper


class TestIMDBTop20Scraper(TestCase):

    def test_scrape_should_assemble_movies_list_correctly(self):

        scraper = IMDBTop20Scraper()
        scraper.title_page_parser = mock.MagicMock(parse_num_of_won_oscars_from_movie_pages=mock.MagicMock(return_value=[0]))

        # ranks, titles, relative_links, ratings, votes
        scraper.top250_page_parser = mock.MagicMock(parse=mock.MagicMock(return_value=[[7], ["Title"], ["link"], [9.8], [30000]]))

        movies = scraper.scrape()
        self.assertEqual(movies[0].rank, 7, "Rank should be correct")
        self.assertEqual(movies[0].title, "Title", "Title should be correct")
        self.assertEqual(movies[0].imdb_rating, 9.8, "IMDB rating should be correct")
        self.assertEqual(movies[0].num_of_votes, 30000, "Number of votes should be correct")
        self.assertEqual(movies[0].title, "Title", "Title should be correct")
