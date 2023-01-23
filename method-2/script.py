import sqlalchemy
import pandas as pd
import json
from datetime import datetime
from sqlalchemy.orm import sessionmaker
import sqlite3
import requests
import twint 

DATABASE_LOCATION = "/mnt/e/Movie-Reccomendation-App/method-2/movies.sqlite"

QUERY = """

c = twint.Config()
c.Search = "I rated* /10 #IMDb"
c.since = datetime.datetime.now().strftime("%Y-%m-%d")
c.until = datetime.datetime.now().strftime("%Y-%m-%d")
c.Format = "id: {id}, created_at: {created_at}, tweet: {tweet}, user_id: {user_id}, likes_count: {likes_count}"
c.Store_object = True
twint.run.Search(c)

"""

def check_if_valid_data(df: pd.DataFrame) -> bool:
    if df.empty:
        print("No tweets downloaded")
        return False

    #Primary key check
    if pd.series(df['id']).is_unique:
        pass
    else:
        raise Exception("Primary key check violated")

    #check for nulls
    if df.isnull().values.any():
        raise Exception("Null values found")


