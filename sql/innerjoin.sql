SELECT repo.tconst as movie_id
,repo.runtimeMinutes
,repo.genres 
,tweet_titles.user_id 
,tweet_titles.unix_time 
,tweet_titles.title 
,tweet_titles."year" 
,tweet_titles.rating 
,repo.startYear 
from tweet_titles 
INNER JOIN repo ON tweet_titles.title=repo.primaryTitle
where tweet_titles."year"=repo.startYear 
