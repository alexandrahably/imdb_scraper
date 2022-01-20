import time
import requests

from imdb_scraper import IMDBScraper


def main():
    t = time.process_time()

    with requests.Session() as session:
        scraper = IMDBScraper(session=session)
        movies = scraper.scrape_top_movies()

    elapsed_time = time.process_time() - t
    print('Elapsed: ' + str(elapsed_time))

    # Printing movie details
    for movie in movies:
        print(movie.rank, '-', movie.title, '||',
              'Rating:', movie.imdb_rating, ',',
              'Votes:', movie.num_of_votes, ',',
              'Awards:', movie.awards)


if __name__ == '__main__':
    main()
