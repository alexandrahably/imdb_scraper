import pandas as pd

from src.imdb.movie import Movie


def write_to_csv_with_original_rating(movies: list[Movie], output_path: str) -> None:
    """
    This function creates a dataframe from the received movies, and saves the so created table to a csv.
    Columns of the csv file: 'IMDB rating', 'Num of votes', 'Num of won Oscars', 'Movie title'
    :param movies: A list of movies that we want to export into a csv
    :param output_path: The file path where the csv will be saved
    :return: None
    """
    df = pd.DataFrame([[f'{m.imdb_rating:.2f}', str(m.num_of_votes), str(m.num_of_won_oscars), m.title] for m in movies],
                      columns=['IMDB rating', 'Num of votes', 'Num of won Oscars', 'Movie title'])
    df.to_csv(output_path, index=False, header=True)


def write_to_csv_with_adjusted_rating(num_of_max_votes: int, movies: list[Movie], output_path: str) -> None:
    """
    This function creates a dataframe from the received movies, and saves the so created table to a csv.
    Columns of the csv file: 'Adjusted rating', 'Num of votes', 'Num of won Oscars', 'Movie title'
    :param movies: A list of movies that we want to export into a csv
    :param output_path: The file path where the csv will be saved
    :return: None
    """
    df = pd.DataFrame([[f'{m.adjusted_rating(num_of_max_votes):.2f}', str(m.num_of_votes), str(m.num_of_won_oscars), m.title] for m in movies],
                      columns=['Adjusted rating', 'Num of votes', 'Num of won Oscars', 'Movie title'])
    df.to_csv(output_path, index=False, header=True)
