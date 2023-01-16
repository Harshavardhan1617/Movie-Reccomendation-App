import logging
from imdb import IMDb
import pandas as pd

# create an instance of the IMDb class
ia = IMDb()

# create an empty column to store the movie ids
cleaned_tweets['movie_id'] = None

# configure logging
logging.basicConfig(filename='movie_idlog.log', level=logging.WARNING)

# loop through the titles and search for each movie on IMDb
for i, title in cleaned_tweets.iterrows():
    try:
        movie = ia.search_movie(title['movie_title'])[0]
        movie_id = movie.movieID
        df.loc[i, 'movie_id'] = movie_id
    except IndexError as e:
        logging.warning(f'No results found for {title["movie_title"]}')
        df.loc[i, 'movie_id'] = None
    except Exception as e:
        logging.warning(f'An error occurred: {e}')
        df.loc[i, 'movie_id'] = None
