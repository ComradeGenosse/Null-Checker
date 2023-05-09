import os
import sqlite3
import unittest
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout

class TestDatabase(unittest.TestCase):

    def setUp(self):
        # Create an in-memory database for testing
        self.conn = sqlite3.connect(':memory:')
        self.c = self.conn.cursor()

        # Create a table for testing
        self.c.execute('''CREATE TABLE test_table
                          (id INTEGER PRIMARY KEY,
                          name TEXT NOT NULL,
                          age INTEGER NOT NULL);''')
        self.c.execute("INSERT INTO test_table (name, age) VALUES ('John', 25)")
        self.c.execute("INSERT INTO test_table (name, age) VALUES ('Bob', NULL)")

        self.conn.commit()

    def tearDown(self):
        self.conn.close()

    def test_null_rows_exported_to_csv(self):
        # Set up the expected output
        expected_output = 'Processing database: :memory:\n1 rows fetched.\nWriting to output/test_table_output.csv\n' \
                          'test_table_output.csv created.\n'
        expected_csv_output = 'id,name,age\n2,Bob,\n'

        # Redirect stdout to capture the output of the main function
        with redirect_stdout(StringIO()) as output:
            with patch('builtins.input', return_value=':memory:'):
                main()

        self.assertEqual(output.getvalue(), expected_output)

        # Check that the CSV file was created and contains the expected data
        with open(os.path.join('output', 'test_table_output.csv')) as f:
            csv_output = f.read()

        self.assertEqual(csv_output, expected_csv_output)

    def test_no_null_rows(self):
        # Add a row without null values
        self.c.execute("INSERT INTO test_table (name, age) VALUES ('Mary', 30)")

        # Set up the expected output
        expected_output = 'Processing database: :memory:\n0 rows fetched.\n'

        # Redirect stdout to capture the output of the main function
        with redirect_stdout(StringIO()) as output:
            with patch('builtins.input', return_value=':memory:'):
                main()

        self.assertEqual(output.getvalue(), expected_output)

        # Check that the output directory was not created
        self.assertFalse(os.path.exists('output'))

    def test_table_with_null_values(self):
        # Create a table with null values
        self.c.execute('''CREATE TABLE test_table_2
                          (id INTEGER PRIMARY KEY,
                          name TEXT NOT NULL,
                          age INTEGER);''')
        self.c.execute("INSERT INTO test_table_2 (name, age) VALUES ('John', NULL)")
        self.c.execute("INSERT INTO test_table_2 (name, age) VALUES ('Bob', 40)")

        self.conn.commit()

        # Set up the expected output
        expected_output = 'Processing database: :memory:\n1 rows fetched.\nWriting to output/test_table_2_output.csv\n' \
                          'test_table_2_output.csv created.\n'
        expected_csv_output = 'id,name,age\n1,John,\n'

        # Redirect stdout to capture the output of the main function
        with redirect_stdout(StringIO()) as output:
            with patch('builtins.input', return_value=':memory:'):
                main()

        self.assertEqual(output.getvalue(), expected_output)

        # Check that the CSV file was created and contains the expected data
        with open(os.path.join('output', 'test_table_2_output.csv')) as f:
            csv_output = f.read()

        self.assertEqual(csv_output, expected_csv_output)
