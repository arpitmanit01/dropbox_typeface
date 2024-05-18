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

    def add_file(self, file_id, filename, mimetype, size, content):
        """Add a file to the database."""
        self.cursor.execute("INSERT INTO files(id,filename,mimetype,size,content)\
                             VALUES (?,?,?,?,?)",
                            (file_id, filename, mimetype, size, sqlite3.Binary(content)))
        self.conn.commit()

    def get_all(self):
        c = self.conn.cursor()
        c.execute(
            '''
            SELECT * FROM files
            '''
        )
        result = c.fetchall()
        return result

    def get_by_id(self, content_unique_id: str):
        c = self.conn.cursor()
        c.execute(
            '''
            SELECT * FROM files AS t
            WHERE t.id=?
            ''', (content_unique_id,)
        )
        result = c.fetchall()
        return result

    def close(self):
        """Close the database connection."""
        self.conn.close()
