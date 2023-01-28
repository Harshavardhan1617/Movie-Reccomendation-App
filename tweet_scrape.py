import twint

c = twint.Config()
c.Search = "I rated* /10 #IMDb"
#c.since = "2021-11-24 05:41:29"
c.Limit = 1500
c.Until = "2021-01-24 05:50:23.000000"

c.Store_csv = True
c.Output = "tweets3.csv"
twint.run.Search(c)


import pandas as pd

# Read CSV file into a DataFrame
#df = pd.read_csv("tweets3.csv")
