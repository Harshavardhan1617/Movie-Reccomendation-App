import pandas as pd
from sqlalchemy import create_engine

# Read the TSV file into a DataFrame
df = pd.read_csv('new_data/data-basic.tsv', delimiter='\t', low_memory=False)
df
# Connect to the SQLite database
engine = create_engine('sqlite:///new_data/movies.sqlite')

# Write the DataFrame to the SQLite database
df.to_sql('repo', engine, if_exists='replace', index=False)
