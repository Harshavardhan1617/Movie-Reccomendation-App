import twint

c = twint.Config()
c.Search = "I rated* /10 #IMDb"
c.since = "2021-11-24 05:41:29"
c.Until = "2023-01-03 16:59:04"

c.Store_csv = True
c.Output = "tweets.csv"
twint.run.Search(c)