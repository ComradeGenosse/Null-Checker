import sqlite3
import csv
import os

# Define the name of your SQLite database file
database_name = "TestDB3.pmx"
print(f"Processing database: {database_name}")

# Define the name of the output directory and output file
output_directory = "output"
output_file = "output.csv"

# Open a connection to the database
connection = sqlite3.connect(database_name)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Get the names of all tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Iterate over each table
for table in tables:
    table_name = table[0]
    
    # Get the column names of the table
    cursor.execute(f"PRAGMA table_info({table_name})")
    column_names = [row[1] for row in cursor.fetchall()]
    
    # Construct the null query
    null_query = f"SELECT * FROM {table_name} WHERE "
    for column_name in column_names:
        null_query += f"{column_name} IS NULL OR "
    null_query = null_query[:-4]  # Remove the last "OR" from the query string
    
    # Execute the query to retrieve rows with null values
    cursor.execute(null_query)
    
    # Fetch all rows that match the query
    null_rows = cursor.fetchall()
    print(f"{len(null_rows)} rows fetched.")
    
    # If there are null value rows, write them to a CSV file
    if len(null_rows) > 0:
        # Create the output directory if it does not exist
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        
        # Write the rows to a CSV file
        output_csv_path = os.path.join(output_directory, f"{table_name}_{output_file}")
        print(f"Writing to {output_csv_path}")
        with open(output_csv_path, mode="w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(column_names)
            writer.writerows(null_rows)
        print(f"{table_name}_{output_file} created.")

# Close the database connection
connection.close()
