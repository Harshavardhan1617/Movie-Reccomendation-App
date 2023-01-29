import sqlalchemy
import pandas as pd
#import json
import datetime
from sqlalchemy.orm import sessionmaker
import sqlite3
#import requests
import twint

DATABASE_LOCATION = "sqlite:////media/harsha/projects/data/imdb/movies_data.sqlite"
#Connecting to sqlite
engine = sqlalchemy.create_engine(DATABASE_LOCATION)
conn = sqlite3.connect('/media/harsha/projects/data/imdb/movies_data.sqlite')
#Creating a cursor object using the cursor() method
cursor = conn.cursor()

old_date = cursor.execute('''
SELECT strftime('%Y-%m-%d %H:%M:%S', MIN(date)) as date
FROM tweets

''')
old_date = cursor.fetchone()[0];


print("the oldest date in database is : ", old_date)

# #validity check
# def check_if_valid_data(df: pd.DataFrame) -> bool:
#     if df.empty:
#         print("No tweets downloaded")
#         return False
#
#     #Primary key check
#     if pd.Series(df['conversation_id']).is_unique:
#         pass
#     else:
#         raise Exception("Primary key check violated")

#extract
c = twint.Config()
c.Search = "I rated* /10 #IMDb"
c.Custom = ["conversation_id", "created_at","tweet", "username", "date", "user_id"]
c.Until = old_date
c.Limit = 2000
c.Pandas = True


twint.run.Search(c)

def twint_to_pd(columns):
    return twint.output.panda.Tweets_df[columns]

tweets_df = twint_to_pd(["conversation_id","tweet", "username", "date", "user_id"])
#tweets_df.to_csv('tweets.csv', index = False)

#df = tweets_df
tweets_df.loc[:, 'tweet'] = tweets_df['tweet'].str.split(" #IMDb", expand=True)[0]
tweets_df['tweet'] = tweets_df['tweet'].str.replace('.*I rated', 'I rated')
tweets_df["date"] = pd.to_datetime(tweets_df["date"])
tweets_df["date"] = tweets_df["date"].dt.strftime('%Y-%m-%d %H:%M:%S')
tweets_df["unix_time"] = pd.to_datetime(tweets_df["date"]).astype(int) / 10**9


# Validate
# if check_if_valid_data(tweets_df):
#     print("Data valid, proceed to Load stage")


#Load
cursor = conn.cursor()

sql_query = """
CREATE TABLE IF NOT EXISTS tweets(
    conversation_id VARCHAR(200),
    tweet VARCHAR(200),
    username VARCHAR(200),
    date VARCHAR(200),
    user_id VARCHAR(200),
    unix_time VARCHAR(200),
    CONSTRAINT primary_key_constraint PRIMARY KEY (conversation_id)
)
"""


cursor.execute(sql_query)
print("Opened database successfully")

try:
    tweets_df.to_sql("tweets", engine, index=False, if_exists='append')
    print("loaded tweets")
except:
    print("Data already exists in the database")

#conn.close()
#print("Close database successfully")

cursor = conn.cursor()
q_extract = """
SELECT ROWID as S_No
,user_id
,username
,tweet
,unix_time
from tweets
WHERE unix_time<(SELECT MIN(unix_time) FROM tweet_titles)

"""

try:
    df = pd.read_sql_query(q_extract, engine)
    print(df.info())
except:
    print("failed to load data")

#dropping null values
df = df.dropna()
print("#after dropping null \n", df.info())

#extracting titles,year and ratings from tweets
df[['title','year','rating']] = df['tweet'].str.extract(r'rated (.*) \((.*)\) (.*)')
print("#after extracting strings", df.info())

#removing null titles
df_2 = df[df['title'].isnull()]
df = df[~df['S_No'].isin(df_2['S_No'])]

#removing tv-shows from titles
df_1 = df[df['year'].str.len()>4]
df = df[~df['S_No'].isin(df_1['S_No'])]
print("#after removing tv-shows", df.info())

df = df.drop('S_No', axis=1)
df.info()

#load
sql_query_2 = """
CREATE TABLE IF NOT EXISTS tweet_titles(
    user_id VARCHAR(200),
    username VARCHAR(200),
    tweet VARCHAR(200),
    unix_time VARCHAR(200),
    title VARCHAR(200),
    year VARCHAR(200),
    rating VARCHAR(200)


)
"""


cursor.execute(sql_query_2)
print("Opened tweet_titles table successfully")

try:
    df.to_sql("tweet_titles", engine, index=False, if_exists='append')
except:
    print("Data already exists in the database")

conn.close()
print("Close database successfully")
