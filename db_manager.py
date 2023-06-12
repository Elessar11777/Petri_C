import sqlite3
import json
import os

# Constants
DB_PATH = "resources/web/aeya.db"
TABLE_NAME = "aeya_register"
JSON_DIRECTORY = "./dumps/"

# Create JSON directory if it doesn't exist
if not os.path.exists(JSON_DIRECTORY):
    os.makedirs(JSON_DIRECTORY)

class DBManager:
    def __init__(self, db_path=DB_PATH, table_name=TABLE_NAME):
        self.db_path = db_path
        self.table_name = table_name

        self.create_db()

    def create_db(self):
        # Setup sqlite connection
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create table if it doesn't exist
        cursor.execute(f'''
                        CREATE TABLE IF NOT EXISTS {self.table_name} (
                                                                    id INTEGER PRIMARY KEY,
                                                                    file_path TEXT NOT NULL,
                                                                    status TEXT NOT NULL
                                                                    )
                        ''')

        # Commit changes and close connection
        conn.commit()
        conn.close()

    def add_db_item(self, json_dict, research="gracia", status="unsent"):
        # Setup sqlite connection
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            time = json_dict["Meta"]["Time"]
        except:
            time = ""
        try:
            bacteria = json_dict["Meta"]["Bacteria"]
        except:
            bacteria = ""
        try:
            code = json_dict["Meta"]["Code"]
            print(code)
        except:
            code = ""
        try:
            if research.lower() == "gracia":
                appendix = json_dict["Meta"]["Dilution"]
            elif research.lower() == "spot":
                appendix = json_dict["Meta"]["Cell"]
            else:
                appendix = ""
        except:
            appendix = ""
        file_path = os.path.join(JSON_DIRECTORY, f"{time}_{bacteria}{code}-{appendix}.json")

        with open(file_path, 'w') as f:
            json.dump(json_dict, f)

        # Insert into table
        cursor.execute(f'''
                        INSERT INTO {self.table_name} (file_path, status)
                        VALUES (?, ?)
                        ''', (file_path, status))
        # Commit changes and close connection
        conn.commit()
        conn.close()

    def load_db_items(self):
        # Setup sqlite connection
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Execute a query to fetch all tables in the database
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        # Loop through all tables
        for table in tables:
            print(f"Table: {table[0]}")

            # Execute a query to select all rows from the current table
            cursor.execute(f"SELECT * FROM {table[0]};")

            # Fetch all rows as a list of tuples
            rows = cursor.fetchall()

            # Print all rows
            for row in rows:
                print(row)

        # Close the connection
        conn.close()
        return rows

    def select_unsent(self):
        # Setup sqlite connection
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Execute a query to select all file_path where status is 'unsent'
        cursor.execute(f"SELECT id, file_path, status FROM {self.table_name} WHERE status = 'unsent';")


        # Fetch all rows as a list of tuples
        rows = cursor.fetchall()

        # Close the connection
        conn.close()

        return rows

    def update_status_to_sent(self, index):
        # Setup sqlite connection
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Execute a query to update status to 'sent' for the specified id
        cursor.execute(f"UPDATE {self.table_name} SET status = 'sent' WHERE id = ?;", (index,))

        # Commit changes and close connection
        conn.commit()
        conn.close()

    def set_status_not_found(self, id):
        # Setup sqlite connection
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Execute a query to update status to 'not found' for the specified id
        cursor.execute(f"UPDATE {self.table_name} SET status = 'not found' WHERE id = ?;", (id,))

        # Commit changes and close connection
        conn.commit()
        conn.close()

    def reset_db(self):
        # Setup sqlite connection
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Drop the table
        cursor.execute(f"DROP TABLE IF EXISTS {self.table_name};")

        # Recreate the table
        self.create_db()

        # Commit changes and close connection
        conn.commit()
        conn.close()
