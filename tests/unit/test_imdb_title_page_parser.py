import pytest
import os
from pathlib import Path
from unittest import TestCase
from tests.unit.helpers.helpers import path_for_resource
from src.imdb.parsers import IMDBTitlePageParser


def movie_without_oscars_page_text():
    movie_page_no_oscars_path = path_for_resource('movie_page_no_oscars.html')
    with open(movie_page_no_oscars_path, "r") as file:
        text = file.read()
        file.close()
        return text


def movie_with_oscars_page_text():
    movie_page_with_oscars_path = path_for_resource('movie_page_with_oscars.txt')
    with open(movie_page_with_oscars_path, "r") as file:
        text = file.read()
        file.close()
        return text


class TestIMDBTitlePageParser(TestCase):

    def test_parse_num_of_won_oscars_from_movie_page_without_oscars(self):
        movie_title_page_no_oscars_text = movie_without_oscars_page_text()
        num_of_oscars = IMDBTitlePageParser.parse_num_of_won_oscars_from_movie_page(movie_title_page_no_oscars_text)
        self.assertEqual(num_of_oscars, 0)

    def test_parse_num_of_won_oscars_from_movie_page_with_oscars(self):
        movie_title_page_with_oscars_text = movie_with_oscars_page_text()
        num_of_oscars = IMDBTitlePageParser.parse_num_of_won_oscars_from_movie_page(movie_title_page_with_oscars_text)
        self.assertEqual(num_of_oscars, 3)
