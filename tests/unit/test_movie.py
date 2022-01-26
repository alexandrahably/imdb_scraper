from unittest import TestCase

from src.imdb.movie import Movie


class TestMovie(TestCase):

    def test_adjusted_rating_is_not_impacted_by_num_of_votes(self):
        movie = Movie(rank=1, title="", imdb_rating=2, num_of_votes=10, num_of_won_oscars=0)
        max_votes = 100009
        adjusted_rating = movie.adjusted_rating(max_votes)
        self.assertEqual(adjusted_rating, movie.imdb_rating,
                         "If there is a less than 100k deviation, no penalty should be applied")

    def test_adjusted_rating_is_impacted_by_num_of_votes_single_100k_deviation(self):
        movie = Movie(rank=1, title="", imdb_rating=2, num_of_votes=9, num_of_won_oscars=0)
        max_votes = 100009
        adjusted_rating = movie.adjusted_rating(max_votes)
        self.assertEqual(adjusted_rating, movie.imdb_rating - 0.1,
                         "A 0.1 penalty should be applied for each 100k deviation.")

    def test_adjusted_rating_is_impacted_by_num_of_votes_multiple_100k_deviation(self):
        movie = Movie(rank=1, title="", imdb_rating=2, num_of_votes=9, num_of_won_oscars=0)
        max_votes = 2000009
        adjusted_rating = movie.adjusted_rating(max_votes)
        self.assertEqual(adjusted_rating, movie.imdb_rating - 2,
                         "A 0.1 penalty should be applied for each 100k deviation.")

    def test_adjusted_rating_cant_be_negative(self):
        movie = Movie(rank=1, title="", imdb_rating=2, num_of_votes=9, num_of_won_oscars=0)
        max_votes = 3000009
        adjusted_rating = movie.adjusted_rating(max_votes)
        self.assertEqual(adjusted_rating, 0, "The adjusted rating can't be negative.")


    def test_adjusted_rating_is_impacted_by_number_of_oscars(self):
        movie = Movie(rank=1, title="", imdb_rating=2, num_of_votes=10, num_of_won_oscars=0)
        max_votes = 10
        adjusted_rating = movie.adjusted_rating(max_votes)
        self.assertEqual(adjusted_rating, movie.imdb_rating,
                         "If there is a less than 100k deviation, and there are no Oscars, no reward should be applied.")


    def test_adjusted_rating_is_impacted_by_number_of_oscars_is_1or2(self):
        max_votes = 10

        movie_1_oscar = Movie(rank=1, title="", imdb_rating=2, num_of_votes=10, num_of_won_oscars=1)
        adjusted_rating1 = movie_1_oscar.adjusted_rating(max_votes)
        self.assertEqual(adjusted_rating1, movie_1_oscar.imdb_rating + 0.3,
                         "If there is a less than 100k deviation, and there is 1 Oscars, 0.3 reward should be applied.")

        movie_2_oscar = Movie(rank=1, title="", imdb_rating=2, num_of_votes=10, num_of_won_oscars=2)
        adjusted_rating1 = movie_2_oscar.adjusted_rating(max_votes)
        self.assertEqual(adjusted_rating1, movie_2_oscar.imdb_rating + 0.3,
                         "If there is a less than 100k deviation, and there are 2 Oscars, 0.3 reward should be applied.")


    def test_adjusted_rating_is_impacted_by_number_of_oscars_is_3to5(self):
        max_votes = 10

        movie_3_oscar = Movie(rank=1, title="", imdb_rating=2, num_of_votes=10, num_of_won_oscars=3)
        adjusted_rating1 = movie_3_oscar.adjusted_rating(max_votes)
        self.assertEqual(adjusted_rating1, movie_3_oscar.imdb_rating + 0.5,
                         "If there is a less than 100k deviation, and there are 3-5 Oscars, 0.5 reward should be applied.")

        movie_5_oscar = Movie(rank=1, title="", imdb_rating=2, num_of_votes=10, num_of_won_oscars=5)
        adjusted_rating1 = movie_5_oscar.adjusted_rating(max_votes)
        self.assertEqual(adjusted_rating1, movie_5_oscar.imdb_rating + 0.5,
                         "If there is a less than 100k deviation, and there are 3-5 Oscars, 0.5 reward should be applied.")

    def test_adjusted_rating_is_impacted_by_number_of_oscars_is_6to10(self):
        max_votes = 10

        movie_6_oscar = Movie(rank=1, title="", imdb_rating=2, num_of_votes=10, num_of_won_oscars=6)
        adjusted_rating1 = movie_6_oscar.adjusted_rating(max_votes)
        self.assertEqual(adjusted_rating1, movie_6_oscar.imdb_rating + 1,
                         "If there is a less than 100k deviation, and there are 6-10 Oscars, 1 reward should be applied.")

        movie_10_oscar = Movie(rank=1, title="", imdb_rating=2, num_of_votes=10, num_of_won_oscars=10)
        adjusted_rating1 = movie_10_oscar.adjusted_rating(max_votes)
        self.assertEqual(adjusted_rating1, movie_10_oscar.imdb_rating + 1,
                         "If there is a less than 100k deviation, and there are 6-10 Oscars, 1 reward should be applied.")

    def test_adjusted_rating_is_impacted_by_number_of_oscars_is_more_than10(self):
        max_votes = 10

        movie_11_oscar = Movie(rank=1, title="", imdb_rating=2, num_of_votes=10, num_of_won_oscars=11)
        adjusted_rating1 = movie_11_oscar.adjusted_rating(max_votes)
        self.assertEqual(adjusted_rating1, movie_11_oscar.imdb_rating + 1.5,
                         "If there is a less than 100k deviation, and there are 10+ Oscars, 1.5 reward should be applied.")

        movie_70_oscar = Movie(rank=1, title="", imdb_rating=2, num_of_votes=10, num_of_won_oscars=70)
        adjusted_rating1 = movie_70_oscar.adjusted_rating(max_votes)
        self.assertEqual(adjusted_rating1, movie_70_oscar.imdb_rating + 1.5,
                         "If there is a less than 100k deviation, and there are 10+ Oscars, 1.5 reward should be applied.")
