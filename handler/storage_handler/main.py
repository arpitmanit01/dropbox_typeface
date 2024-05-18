# Importing the sqlite3 module to interact with SQLite databases
import sqlite3

# Defining a class named StorageHandler to manage storage operations
class StorageHandler:
    # Constructor method initializing the database path, connection, cursor, and calling the init_db method
    def __init__(self):
        self.db_path = ':memory:'  # Using an in-memory database for simplicity
        self.conn = None
        self.cursor = None
        self.init_db()

    # Method to initialize the database connection and cursor
    def init_db(self):
        """Initialize the database."""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)  # Connect to the database
        self.cursor = self.conn.cursor()  # Initialize the cursor object

        # Call the create_table method to ensure the table structure is set up
        self.create_table()

    # Method to create the table structure if it doesn't exist
    def create_table(self):
        try:
            """Create the table for storing file metadata and content."""
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS files (
                                    id TEXT PRIMARY KEY,
                                    filename TEXT NOT NULL,
                                    mimetype TEXT NOT NULL,
                                    size INTEGER NOT NULL,
                                    content BLOB NOT NULL,
                                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                                )''')  # SQL command to create the table
            self.conn.commit()  # Commit the transaction
        except Exception as e:
            print(str(e))  # Print error message if any exception occurs

    # Method to add a file to the database
    def add_file(self, file_id: str, filename: str, mimetype: str, size: int, content):
        """Add a file to the database."""
        try:
            self.cursor.execute("INSERT INTO files(id,filename,mimetype,size,content)\
                                 VALUES (?,?,?,?,?)",  # SQL command to insert a new row
                                (file_id, filename, mimetype, size, sqlite3.Binary(content)))  # Parameters for the INSERT statement
            self.conn.commit()  # Commit the transaction
        except Exception as e:
            print(str(e))  # Print error message if any exception occurs

    # Method to retrieve all records from the files table
    def get_all(self):
        try:
            c = self.conn.cursor()
            c.execute(
                '''
                SELECT id,filename,mimetype,created_at FROM files
                '''
            )
            result = c.fetchall()
            return result
        except Exception as e:
            print(str(e))  # Print error message if any exception occurs

    # Method to retrieve a record by its unique ID
    def get_by_id(self, content_unique_id: str):
        try:
            c = self.conn.cursor()
            c.execute(
                '''
                SELECT id,filename,mimetype,created_at FROM files AS t
                WHERE t.id=?
                ''', (content_unique_id,)  # Parameter for the WHERE clause
            )
            result = c.fetchall()
            return result
        except Exception as e:
            print(str(e))  # Print error message if any exception occurs

    # Method to update a file's name by its unique ID
    def update_by_id(self, content_unique_id: str, new_file_name: str):
        try:
            c = self.conn.cursor()
            c.execute(
                '''
                UPDATE files 
                SET filename=?
                WHERE id=?
                ''', (new_file_name, content_unique_id,)  # Parameters for the UPDATE statement
            )
            self.conn.commit()  # Commit the transaction
            return None
        except Exception as e:
            print(str(e))  # Print error message if any exception occurs

    # Method to delete a file by its unique ID
    def delete_by_id(self, content_unique_id: str):
        try:
            c = self.conn.cursor()
            c.execute(
                '''
                DELETE FROM files AS t
                WHERE t.id=?
                ''', (content_unique_id,)  # Parameter for the WHERE clause
            )
            self.conn.commit()  # Commit the transaction
            return None
        except Exception as e:
            print(str(e))  # Print error message if any exception occurs

    # Method to close the database connection
    def close(self):
        try:
            """Close the database connection."""
            self.conn.close()  # Close the connection
        except Exception as e:
            print(str(e))  # Print error message if any exception occurs
