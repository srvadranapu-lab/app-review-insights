import argparse
from app.ingestion import fetch_all_reviews
from app.database import db
from app.processing import load_reviews, filter_reviews, prepare_llm_input, save_processed_reviews
from app.summarize import generate_summary
from app.render import load_summary, generate_report, generate_email, save_report, save_email
from app.publish_docs import publish_to_docs
from app.publish_email import publish_email

def run():
    print("Pipeline not implemented yet")

def ingest():
    print("Fetching reviews...")
    reviews = fetch_all_reviews("groww")
    print(f"Fetched {len(reviews)} reviews")
    
    print("Inserting reviews into database...")
    inserted_count = db.insert_reviews(reviews)
    print(f"Inserted {inserted_count} new reviews")

def process():
    print("Loading reviews...")
    reviews = load_reviews("groww")
    print(f"Loaded {len(reviews)} reviews")
    
    print("Filtering reviews...")
    filtered_reviews = filter_reviews(reviews)
    print(f"After filtering: {len(filtered_reviews)} reviews")
    
    print("Preparing LLM input...")
    llm_input = prepare_llm_input(filtered_reviews)
    print(f"Prepared {len(llm_input)} reviews for LLM")
    
    print("Saving processed reviews...")
    save_processed_reviews(llm_input)
    print("Saved to data/processed_reviews.json")

def summarize():
    result = generate_summary()
    if result:
        print(f"Generated {len(result.get('themes', []))} themes")
        print(f"Found {len(result.get('quotes', []))} valid quotes")
        print(f"Created {len(result.get('actions', []))} action ideas")

def render():
    print("Loading summary...")
    summary = load_summary()
    
    if not summary:
        print("Error: No summary found. Run 'python -m app.cli summarize' first.")
        return
    
    print("Generating report...")
    report = generate_report(summary, "Groww")
    save_report(report)
    print("Report saved to data/report.txt")
    
    print("Generating email...")
    subject, body = generate_email(summary, "Groww")
    save_email(subject, body)
    print("Email saved to data/email.html")
    
    print("Rendering complete!")

def publish_docs():
    doc_link = publish_to_docs()
    if doc_link:
        print(f"Published to Google Docs: {doc_link}")

def publish_email_cmd():
    success = publish_email()
    if success:
        print("Email published successfully!")

def main():
    parser = argparse.ArgumentParser(description="App Review Insights Analyser CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run the review analysis pipeline")
    
    # Ingest command
    ingest_parser = subparsers.add_parser("ingest", help="Ingest reviews from app stores")
    
    # Process command
    process_parser = subparsers.add_parser("process", help="Process and clean reviews for LLM")
    
    # Summarize command
    summarize_parser = subparsers.add_parser("summarize", help="Generate insights using LLM")
    
    # Render command
    render_parser = subparsers.add_parser("render", help="Generate report and email")
    
    # Publish docs command
    publish_docs_parser = subparsers.add_parser("publish_docs", help="Publish report to Google Docs")
    
    # Publish email command
    publish_email_parser = subparsers.add_parser("publish_email", help="Send email via Gmail MCP")
    
    args = parser.parse_args()
    
    if args.command == "run":
        run()
    elif args.command == "ingest":
        ingest()
    elif args.command == "process":
        process()
    elif args.command == "summarize":
        summarize()
    elif args.command == "render":
        render()
    elif args.command == "publish_docs":
        publish_docs()
    elif args.command == "publish_email":
        publish_email_cmd()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
