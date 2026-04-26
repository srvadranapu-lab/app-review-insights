import requests
import re
from datetime import datetime
from typing import List, Dict
from google_play_scraper import Sort, reviews

def scrub_pii(text: str) -> str:
    """Remove emails and phone numbers from text."""
    # Remove email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
    # Remove 10-digit phone numbers
    text = re.sub(r'\b\d{10}\b', '[PHONE]', text)
    return text

def fetch_appstore_reviews(product_name: str) -> List[Dict]:
    """Fetch reviews from App Store RSS feed."""
    app_ids = {
        "groww": "1472870897"
    }
    
    app_id = app_ids.get(product_name)
    if not app_id:
        raise ValueError(f"Unsupported product: {product_name}")
    
    url = f"https://itunes.apple.com/rss/customerreviews/id={app_id}/sortby=mostrecent/json"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        reviews = []
        entries = data.get("feed", {}).get("entry", [])
        
        for entry in entries[1:]:  # Skip first entry (feed info)
            if "im:rating" in entry and "title" in entry and "content" in entry:
                review_id = entry.get("id", {}).get("label", "").split("/")[-1]
                rating = int(entry.get("im:rating", {}).get("label", 0))
                title = entry.get("title", {}).get("label", "")
                body = entry.get("content", {}).get("label", "")
                date_str = entry.get("updated", {}).get("label", "")
                
                # Parse date
                try:
                    date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                    date_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    date_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                reviews.append({
                    "id": f"appstore_{review_id}",
                    "product": product_name,
                    "source": "appstore",
                    "rating": rating,
                    "title": scrub_pii(title),
                    "body": scrub_pii(body),
                    "date": date_str
                })
        
        return reviews
        
    except Exception as e:
        print(f"Error fetching App Store reviews: {e}")
        return []

def fetch_playstore_reviews(package_name: str) -> List[Dict]:
    """Fetch reviews from Google Play Store."""
    packages = {
        "groww": "com.nextbillion.groww"
    }
    
    package = packages.get(package_name.split("_")[0])  # Extract product name
    if not package:
        raise ValueError(f"Unsupported product: {package_name}")
    
    try:
        result, continuation_token = reviews(
            package,
            lang='en',
            country='us',
            sort=Sort.NEWEST,
            count=100,
            filter_score_with=None
        )
        
        review_list = []
        for review in result:
            review_id = review.get("reviewId", "")
            rating = review.get("score", 0)
            title = review.get("title", "")
            body = review.get("content", "")
            date_obj = review.get("at", datetime.now())
            
            review_list.append({
                "id": f"playstore_{review_id}",
                "product": package_name.split("_")[0],
                "source": "playstore",
                "rating": rating,
                "title": scrub_pii(title),
                "body": scrub_pii(body),
                "date": date_obj.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return review_list
        
    except Exception as e:
        print(f"Error fetching Play Store reviews: {e}")
        return []

def fetch_all_reviews(product_name: str) -> List[Dict]:
    """Fetch reviews from both App Store and Play Store."""
    appstore_reviews = fetch_appstore_reviews(product_name)
    playstore_reviews = fetch_playstore_reviews(product_name)
    
    return appstore_reviews + playstore_reviews
