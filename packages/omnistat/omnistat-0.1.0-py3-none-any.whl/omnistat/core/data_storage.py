import sqlite3

class DataStorage:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)

    def execute_query(self, query, params=None):
        cursor = self.conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self.conn.commit()
        return cursor.fetchall()

    def close(self):
        self.conn.close()