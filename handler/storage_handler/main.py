import sqlite3


class StorageHandler:
    def __init__(self):
        self.db_path = ':memory:'  # Use in-memory database for simplicity
        self.conn = None
        self.cursor = None
        self.init_db()

    def init_db(self):
        """Initialize the database."""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()

        # Create table if not exists
        self.create_table()

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
                                )''')
            self.conn.commit()
        except Exception as e:
            print(str(e))

    def add_file(self, file_id: str, filename: str, mimetype: str, size: int, content):
        """Add a file to the database."""
        try:
            self.cursor.execute("INSERT INTO files(id,filename,mimetype,size,content)\
                                 VALUES (?,?,?,?,?)",
                                (file_id, filename, mimetype, size, sqlite3.Binary(content)))
            self.conn.commit()
        except Exception as e:
            print(str(e))

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
            print(str(e))


def get_by_id(self, content_unique_id: str):
    try:
        c = self.conn.cursor()
        c.execute(
            '''
            SELECT id,filename,mimetype,created_at FROM files AS t
            WHERE t.id=?
            ''', (content_unique_id,)
        )
        result = c.fetchall()
        return result
    except Exception as e:
        print(str(e))


def update_by_id(self, content_unique_id: str, new_file_name: str):
    try:
        c = self.conn.cursor()
        c.execute(
            '''
            UPDATE files 
            SET filename=?
            WHERE id=?
            ''', (new_file_name, content_unique_id,)
        )
        self.conn.commit()
        return None
    except Exception as e:
        print(str(e))


def delete_by_id(self, content_unique_id: str):
    try:
        c = self.conn.cursor()
        c.execute(
            '''
            DELETE FROM files AS t
            WHERE t.id=?
            ''', (content_unique_id,)
        )
        self.conn.commit()
        return None
    except Exception as e:
        print(str(e))


def close(self):
    try:
        """Close the database connection."""
        self.conn.close()
    except Exception as e:
        print(str(e))
