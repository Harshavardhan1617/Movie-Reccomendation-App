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

q_extract = """
SELECT ROWID as S_No
,user_id
,username
,tweet
,unix_time
from tweets

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
sql_query = """
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


cursor.execute(sql_query)
print("Opened database successfully")

try:
    df.to_sql("tweet_titles", engine, index=False, if_exists='append')
except:
    print("Data already exists in the database")

conn.close()
print("Close database successfully")
# #Load
# #cursor = conn.cursor()
#
# sql_query = """
# CREATE TABLE IF NOT EXISTS tweet_titles(
#     user_id VARCHAR(200),
#     username VARCHAR(200),
#     tweet VARCHAR(200),
#     unix_time VARCHAR(200),
#     title VARCHAR(200),
#     year VARCHAR(200),
#     rating VARCHAR(200),
#
# )
# """
# #     CONSTRAINT primary_key_constraint PRIMARY KEY (conversation_id)
#
# cursor.execute(sql_query)
# print("Opened database successfully")
#
# try:
#     tweets_df.to_sql("tweet_titles", engine, index=False, if_exists='append')
# except:
#     print("Data already exists in the database")
#
# conn.close()
# print("Close database successfully")
