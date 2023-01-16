from imdb import IMDb
import pandas as pd

# create an instance of the IMDb class
ia = IMDb()

# create a dataframe with a column 'title' containing movie titles
df = pd.DataFrame({'title': ['The Shawshank Redemption', 'The Godfather', 'The Dark Knight','Argentina, 1985','2 or 3 Things I Know About Her','Нет','The Worst Person in the World']})

# create an empty column to store the movie ids
df['movie_id'] = None

# loop through the titles and search for each movie on IMDb
for i, title in df.iterrows():
    movie = ia.search_movie(title['title'])[0]
    movie_id = movie.movieID
    df.loc[i, 'movie_id'] = movie_id

print(df)
