import sqlite3
import os
from typing import Optional

class Database:
    def __init__(self, db_path: str = "data/app.db"):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.init_db()
    
    def get_connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)
    
    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create reviews table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reviews (
                    id TEXT PRIMARY KEY,
                    product TEXT,
                    source TEXT,
                    rating INTEGER,
                    title TEXT,
                    body TEXT,
                    date TEXT
                )
            """)
            
            # Create runs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS runs (
                    run_id TEXT PRIMARY KEY,
                    product TEXT,
                    week TEXT,
                    status TEXT
                )
            """)
            
            # Create summaries table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS summaries (
                    run_id TEXT PRIMARY KEY,
                    content TEXT
                )
            """)
            
            conn.commit()
    
    def insert_reviews(self, reviews: list):
        """Insert reviews into database with deduplication."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            for review in reviews:
                cursor.execute("""
                    INSERT OR IGNORE INTO reviews 
                    (id, product, source, rating, title, body, date)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    review["id"],
                    review["product"],
                    review["source"],
                    review["rating"],
                    review["title"],
                    review["body"],
                    review["date"]
                ))
            
            conn.commit()
            return cursor.rowcount

# Global database instance
db = Database()
