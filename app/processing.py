import json
import sqlite3
from datetime import datetime
from typing import List, Dict
from app.database import db

def load_reviews(product: str) -> List[Dict]:
    """Fetch all reviews for the given product from SQLite."""
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, product, source, rating, title, body, date 
            FROM reviews 
            WHERE product = ?
            ORDER BY date DESC
        """, (product,))
        
        columns = [description[0] for description in cursor.description]
        reviews = []
        
        for row in cursor.fetchall():
            review = dict(zip(columns, row))
            reviews.append(review)
        
        return reviews

def filter_reviews(reviews: List[Dict]) -> List[Dict]:
    """Apply filters to reviews: English-only and minimum length."""
    filtered = []
    
    for review in reviews:
        body = review.get("body", "")
        
        # Check minimum length (≥20 characters)
        if len(body.strip()) < 20:
            continue
        
        # Check if review is primarily English (≥70% ASCII characters)
        if body:
            ascii_count = sum(1 for char in body if ord(char) < 128)
            ascii_ratio = ascii_count / len(body)
            if ascii_ratio < 0.7:
                continue
        
        filtered.append(review)
    
    return filtered

def prepare_llm_input(reviews: List[Dict]) -> List[Dict]:
    """Prepare reviews for LLM input: limit to 120, sort by newest, keep rating and body."""
    # Sort by date (newest first) - already sorted in load_reviews, but ensure here
    sorted_reviews = sorted(reviews, key=lambda x: x.get("date", ""), reverse=True)
    
    # Limit to max 120 reviews
    limited_reviews = sorted_reviews[:120]
    
    # Prepare LLM input with only rating and body
    llm_input = []
    for review in limited_reviews:
        llm_input.append({
            "rating": review.get("rating", 0),
            "text": review.get("body", "")
        })
    
    return llm_input

def save_processed_reviews(processed_reviews: List[Dict], filepath: str = "data/processed_reviews.json"):
    """Save processed reviews to JSON file."""
    import os
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(processed_reviews, f, ensure_ascii=False, indent=2)
