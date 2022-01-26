import pytest

from unittest import TestCase
from tests.unit.helpers.helpers import path_for_resource
from src.imdb.parsers import IMDBTop250PageParser


def load_top250_page_text():
    top250_page = path_for_resource('top250_page.txt')
    with open(top250_page, "r") as file:
        text = file.read()
        file.close()
        return str(text)


class TestIMDBTop250PageParser(TestCase):

    def test_parse_top250_page(self):
        selection_number = 20
        parser = IMDBTop250PageParser(top_selection_number=selection_number)
        top250_page_text = load_top250_page_text()
        ranks, titles, relative_links, ratings, votes = parser.parse(top250_page_text)
        self.assertEqual(ranks[-1],selection_number)
        self.assertEqual(titles[10], "Fight Club")
        self.assertEqual(relative_links[18], "/title/tt0047478/")
        self.assertEqual(ratings[3], 8.97668223237052)
        self.assertEqual(votes[0], 2532909)


