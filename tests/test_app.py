from unittest import TestCase, mock
from unittest.mock import patch

import src.imdb.utils as utils
from src.app import main, ORIGINAL_RANKING_OUTPUT_PATH, ADJUSTED_RANKING_OUTPUT_PATH


class AppTest(TestCase):

    @patch('src.imdb.utils.write_to_csv_with_adjusted_rating')
    @patch('src.imdb.utils.write_to_csv_with_original_rating')
    @patch('src.imdb.scraper.IMDBTop20Scraper.scrape')
    def test_movies_original_ranking_is_written_to_file(self, mock_scraper, mock_utils_original, mock_utils_adjusted):

        mock_max_value_of_votes = 9
        mock_movies = []
        for i in range(1, 11):
            mock_movie = mock.Mock(adjusted_rating=mock.MagicMock(return_value=11 - i))
            type(mock_movie).num_of_votes = mock.PropertyMock(return_value=mock_max_value_of_votes)
            type(mock_movie).imdb_rating = mock.PropertyMock(return_value=i)
            mock_movies.append(mock_movie)

        mock_scraper.return_value = mock_movies

        mock_utils_original.return_value = mock.MagicMock(return_value=None)
        mock_utils_adjusted.return_value = mock.MagicMock(return_value=None)

        main()

        mock_movies_in_adjusted_order = sorted(mock_movies, key=lambda m: m.adjusted_rating(), reverse=True)
        mock_utils_original.assert_called_once_with(mock_movies, ORIGINAL_RANKING_OUTPUT_PATH)
        mock_utils_adjusted.assert_called_once_with(mock_max_value_of_votes, mock_movies_in_adjusted_order, ADJUSTED_RANKING_OUTPUT_PATH)
