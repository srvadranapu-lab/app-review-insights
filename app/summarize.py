import json
import os
from app.llm import call_groq, create_prompt, validate_quotes

def generate_summary():
    """Generate summary from processed reviews using LLM."""
    # Load processed reviews
    processed_file = "data/processed_reviews.json"
    if not os.path.exists(processed_file):
        print("Error: processed_reviews.json not found. Run 'python -m app.cli process' first.")
        return
    
    with open(processed_file, 'r', encoding='utf-8') as f:
        reviews = json.load(f)
    
    if not reviews:
        print("Error: No reviews to process.")
        return
    
    print("Generating insights with LLM...")
    
    # Create prompt and call LLM
    prompt = create_prompt(reviews)
    result = call_groq(prompt)
    
    # Validate quotes
    if result.get("quotes"):
        original_quotes = result["quotes"]
        valid_quotes = validate_quotes(original_quotes, reviews)
        result["quotes"] = valid_quotes
        print(f"Quote validation: {len(original_quotes)} -> {len(valid_quotes)} valid quotes")
    
    # Save summary
    summary_file = "data/summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"Summary saved to {summary_file}")
    return result
