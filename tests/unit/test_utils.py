
from unittest import TestCase, mock

from src.imdb.utils import write_to_csv_with_original_rating, write_to_csv_with_adjusted_rating


class Test(TestCase):

    def test_write_to_csv_with_original_rating_calls_pandas_to_csv_with_correct_args(self):
        mock_max_value_of_votes = 9
        mock_movies = []
        for i in range(1, 11):
            mock_movie = mock.Mock(adjusted_rating=mock.MagicMock(return_value=11 - i))
            type(mock_movie).num_of_votes = mock.PropertyMock(return_value=mock_max_value_of_votes)
            type(mock_movie).imdb_rating = mock.PropertyMock(return_value=i)
            mock_movies.append(mock_movie)

        output_file_name = "test.csv"
        with mock.patch("pandas.DataFrame.to_csv") as to_csv_mock:
            write_to_csv_with_original_rating(mock_movies, output_file_name)
            to_csv_mock.assert_called_once_with(output_file_name, index=False, header=True)

    def test_write_to_csv_with_adjusted_rating_calls_pandas_to_csv_with_correct_args(self):
        mock_max_value_of_votes = 9
        mock_movies = []
        for i in range(1, 11):
            mock_movie = mock.Mock(adjusted_rating=mock.MagicMock(return_value=11 - i))
            type(mock_movie).num_of_votes = mock.PropertyMock(return_value=mock_max_value_of_votes)
            type(mock_movie).imdb_rating = mock.PropertyMock(return_value=i)
            mock_movies.append(mock_movie)

        output_file_name = "test.csv"
        with mock.patch("pandas.DataFrame.to_csv") as to_csv_mock:
            write_to_csv_with_adjusted_rating(mock_max_value_of_votes, mock_movies, output_file_name)
            to_csv_mock.assert_called_once_with(output_file_name, index=False, header=True)
