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

    max_votes = max(map(lambda m: m.num_of_votes, movies))

    # Printing movie details
    print('Original order:')
    for movie in movies:
        print(movie.rank, '-', movie.title, '||',
              'Rating:', movie.imdb_rating, ',',
              'Adjusted rating:', str(movie.adjusted_rating(max_votes)))

    print('\nOrder based on the adjusted rating:')
    movies_new_rating = sorted(movies, key=lambda m: m.adjusted_rating(max_votes), reverse=True)
    for movie in movies_new_rating:
        print(movie.rank, '-', movie.title, '||',
              'Rating:', movie.imdb_rating, ',',
              'Adjusted rating:', str(movie.adjusted_rating(max_votes)))


if __name__ == '__main__':
    main()
