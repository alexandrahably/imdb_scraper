# IMDB Scraper

This app scrapes IMDB's website to retrieve the top 20 movies, and saves them in a descending order to csv files, based on:
- their original IMDB rating
- an adjusted rating, that takes into account: 
  - the number of won Oscars (if there are any) as rewards and 
  - the number of the received votes (if it is remarkably small) as penalties 
    
It can be run locally and by using Docker. 


### Running the app locally

Run the following command from the project root:

```bash
pip3 install -r ./requirements.txt
python3 -m src.app
```


### Running the app using Docker

Run the following commands from the project root.

1. Build a Docker image:

```bash
docker build -t imdb_scraper .
```

2. Run the image:

```bash
docker run imdb_scraper
```

### Running the tests

Run the following commands from the project root.

To run all the unit tests

```bash
pytest --cov=./tests/unit/
```

To run all the integration tests

```bash
pytest --cov=./tests/integration/
```

