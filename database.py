import sqlite3

class Database:
    def __init__(self, path: str):
        self.path = path

    def create_tables(self):
        with sqlite3.connect(self.path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS complaints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    instagram_account TEXT,
                    user_complaint TEXT
                )
            """)
            conn.commit()

    def save_complaints(self, data: dict):
        with sqlite3.connect(self.path) as conn:
            conn.execute("""
                INSERT INTO complaints (name, instagram_account, user_complaint)
                VALUES (?, ?, ?)
            """, (data["name"],data["instagram_account"],data["user_complaint"])
                         )
            conn.commit()
