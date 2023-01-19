from imdb import IMDb
import pandas as pd

# create an instance of the IMDb class
ia = IMDb()

# create a dataframe with a column 'title' containing movie titles
#df = pd.DataFrame({'title': ['The Shawshank Redemption', 'The Godfather', 'The Dark Knight','Argentina, 1985','2 or 3 Things I Know About Her','Нет','The Worst Person in the World','Пиноккио Гильермо дель Торо']})

#df = pd.read_csv('movies.csv')

# create an empty column to store the movie ids
final_tweets['movie_id'] = None

# loop through the titles and search for each movie on IMDb
for i, title in final_tweets.iterrows():
    movie = ia.search_movie(title['movie_title'])[1]
    movie_id = movie.movieID
    final_tweets.loc[i, 'movie_id'] = movie_id

logging.basicConfig(filename='id.log', level=logging.WARNING)

# loop through the titles and search for each movie on IMDb
for i, title in final_tweets.iterrows():
    try:
        movie = ia.search_movie(title['movie_title'])[1]
        movie_id = movie.movieID
        final_tweets.loc[i, 'movie_id'] = movie_id
    except IndexError as e:
        logging.warning(f'No results found for {title["movie_title"]}')
        final_tweets.loc[i, 'movie_id'] = None
    except Exception as e:
        logging.warning(f'An error occurred: {e}')
        final_tweets.loc[i, 'movie_id'] = None

final_tweets.to_csv('movie_id.csv')

final_tweets
