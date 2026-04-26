import json
import requests
from app.config import Config

def call_groq(prompt: str) -> dict:
    """Call Groq API with the given prompt and return JSON response."""
    Config.validate()
    
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {Config.GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "system",
                "content": "You are an expert at analyzing app reviews. Always respond with valid JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "response_format": {"type": "json_object"},
        "max_tokens": 500,
        "temperature": 0.3
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        return json.loads(content)
        
    except requests.exceptions.RequestException as e:
        print(f"Error calling Groq API: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response body: {e.response.text}")
        return {"themes": [], "quotes": [], "actions": []}
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
        return {"themes": [], "quotes": [], "actions": []}
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {"themes": [], "quotes": [], "actions": []}

def create_prompt(reviews: list) -> str:
    """Create prompt for LLM based on processed reviews."""
    reviews_text = "\n".join([
        f"Rating: {r['rating']}, Review: {r['text']}" 
        for r in reviews[:50]  # Limit to first 50 for context
    ])
    
    prompt = f"""
Analyze these app reviews and extract insights:

{reviews_text}

Instructions:
1. Group reviews into themes (max 5)
2. Return only top 3 themes
3. Extract EXACT quotes from reviews (must be exact substrings)
4. Generate 3 actionable ideas

Rules:
- Quotes MUST be exact substrings from the input
- Total output ≤250 words
- JSON format only

Output format:
{{
  "themes": ["theme1", "theme2", "theme3"],
  "quotes": ["exact quote1", "exact quote2", "exact quote3"],
  "actions": ["action1", "action2", "action3"]
}}
"""
    return prompt

def validate_quotes(quotes: list, reviews: list) -> list:
    """Ensure each quote exists in at least one review text."""
    valid_quotes = []
    all_texts = [review['text'] for review in reviews]
    
    for quote in quotes:
        for text in all_texts:
            if quote in text:
                valid_quotes.append(quote)
                break
    
    return valid_quotes
