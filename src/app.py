import os
from pathlib import Path
from src.imdb.scraper import IMDBTop20Scraper
import src.imdb.utils as utils

OUTPUT_FOLDER_PATH = Path(os.path.dirname(os.path.realpath(__file__))).parent / 'out'
ORIGINAL_RANKING_OUTPUT_PATH = str(OUTPUT_FOLDER_PATH) + '/original_ranking.csv'
ADJUSTED_RANKING_OUTPUT_PATH = str(OUTPUT_FOLDER_PATH) + '/adjusted_ranking.csv'


def main():
    with IMDBTop20Scraper() as top20_scraper:
        movies = top20_scraper.scrape()

    max_votes = max(movies, key=lambda m: m.num_of_votes).num_of_votes

    # Write to csv: movies in order of original rating (descending)
    utils.write_to_csv_with_original_rating(movies, ORIGINAL_RANKING_OUTPUT_PATH)

    # Write to csv: movies in order of adjusted rating (descending)
    movies_new_ranking = sorted(movies, key=lambda m: m.adjusted_rating(max_votes), reverse=True)
    utils.write_to_csv_with_adjusted_rating(max_votes, movies_new_ranking, ADJUSTED_RANKING_OUTPUT_PATH)
    print("Scraping done. The generated csv files are available in the 'out' folder of the root directory.")


if __name__ == '__main__':
    main()
