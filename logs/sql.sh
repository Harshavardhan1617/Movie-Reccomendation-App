#!/bin/bash

# Set the path to the SQLite database file
DB_FILE="/mnt/e/data/imdb/movies_data.sqlite"

# Set the SQL query to run
SQL_QUERY="SELECT COUNT(*) ,MAX(date) as newest_date ,MIN(date) as oldest_date from tweets"

# Set the path to the log file
LOG_FILE="/mnt/e/Movie-Reccomendation-App/logs/query_results_$(date +\%Y-\%m-\%d_\%H:\%M:\%S).txt"

# Run the query and output the results to the log file
sqlite3 $DB_FILE "$SQL_QUERY" > $LOG_FILE
