import os
import time
import requests
import imdb_scraper.utils as utils
from imdb_scraper.imdb import IMDBTop20Scraper, WebpageDownloader
import os

OUTPUT_FOLDER_PATH = os.getcwd() + '/out/'


def run():
    t = time.process_time()

    with requests.Session() as session:
        page_downloader = WebpageDownloader(session=session)
        top20_scraper = IMDBTop20Scraper(page_downloader=page_downloader)
        movies = top20_scraper.scrape()

    elapsed_time = time.process_time() - t
    print('Elapsed: ' + str(elapsed_time))

    max_votes = max(map(lambda m: m.num_of_votes, movies))

    # Write to csv: movies in order of original rating (descending)
    original_ranking_filepath = OUTPUT_FOLDER_PATH + 'original_ranking.csv'
    utils.write_to_csv_with_original_rating(movies, original_ranking_filepath)

    # Write to csv: movies in order of adjusted rating (descending)
    movies_new_ranking = sorted(movies, key=lambda m: m.adjusted_rating(max_votes), reverse=True)
    adjusted_ranking_filepath = OUTPUT_FOLDER_PATH + 'adjusted_ranking.csv'
    utils.write_to_csv_with_adjusted_rating(max_votes, movies_new_ranking, adjusted_ranking_filepath)


if __name__ == '__main__':
    run()
