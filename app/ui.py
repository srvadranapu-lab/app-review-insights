import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from app.ingestion import fetch_all_reviews
from app.database import db
from app.processing import load_reviews, filter_reviews, prepare_llm_input, save_processed_reviews
from app.summarize import generate_summary
from app.render import load_summary, generate_report, generate_email, save_report, save_email
from app.publish_docs import publish_to_docs
from app.publish_email import publish_email

st.set_page_config(page_title="App Review Insights Analyser", page_icon="📊")

st.title("App Review Insights Analyser")

st.header("Pipeline Steps")

# Ingestion
if st.button("Run Ingestion"):
    with st.spinner("Fetching reviews..."):
        reviews = fetch_all_reviews("groww")
        st.success(f"Fetched {len(reviews)} reviews")
    
    with st.spinner("Inserting reviews into database..."):
        inserted_count = db.insert_reviews(reviews)
        st.success(f"Inserted {inserted_count} new reviews")

# Process Reviews
if st.button("Process Reviews"):
    with st.spinner("Loading reviews..."):
        reviews = load_reviews("groww")
        st.success(f"Loaded {len(reviews)} reviews")
    
    with st.spinner("Filtering reviews..."):
        filtered_reviews = filter_reviews(reviews)
        st.success(f"After filtering: {len(filtered_reviews)} reviews")
    
    with st.spinner("Preparing LLM input..."):
        llm_input = prepare_llm_input(filtered_reviews)
        st.success(f"Prepared {len(llm_input)} reviews for LLM")
    
    with st.spinner("Saving processed reviews..."):
        save_processed_reviews(llm_input)
        st.success("Saved to data/processed_reviews.json")

# Generate Insights
if st.button("Generate Insights"):
    with st.spinner("Generating insights with LLM..."):
        result = generate_summary()
        if result:
            st.success(f"Generated {len(result.get('themes', []))} themes")
            st.success(f"Found {len(result.get('quotes', []))} valid quotes")
            st.success(f"Created {len(result.get('actions', []))} action ideas")

# Generate Report
if st.button("Generate Report"):
    with st.spinner("Loading summary..."):
        summary = load_summary()
        if not summary:
            st.error("No summary found. Run 'Generate Insights' first.")
        else:
            st.success("Summary loaded")
    
    if summary:
        with st.spinner("Generating report..."):
            report = generate_report(summary, "Groww")
            save_report(report)
            st.success("Report saved to data/report.txt")
        
        with st.spinner("Generating email..."):
            subject, body = generate_email(summary, "Groww")
            save_email(subject, body)
            st.success("Email saved to data/email.html")

# Publish to Google Docs
if st.button("Publish to Google Docs"):
    with st.spinner("Publishing to Google Docs..."):
        doc_link = publish_to_docs()
        if doc_link:
            st.success(f"Published to Google Docs: {doc_link}")
        else:
            st.error("Failed to publish to Google Docs")

# Send Email
if st.button("Send Email"):
    with st.spinner("Sending email..."):
        success = publish_email()
        if success:
            st.success("Email sent successfully!")
        else:
            st.error("Failed to send email")

st.header("Outputs")

# Display Report
st.subheader("Report")
if os.path.exists("data/report.txt"):
    with open("data/report.txt", 'r', encoding='utf-8') as f:
        st.text(f.read())
else:
    st.info("Report not generated yet")

# Display Email Preview
st.subheader("Email Preview")
if os.path.exists("data/email.html"):
    with open("data/email.html", 'r', encoding='utf-8') as f:
        st.markdown(f.read())
else:
    st.info("Email not generated yet")

# Display Google Doc Link
st.subheader("Google Doc Link")
if os.path.exists("data/doc_link.txt"):
    with open("data/doc_link.txt", 'r', encoding='utf-8') as f:
        doc_link = f.read().strip()
        st.markdown(f"[Open Google Doc]({doc_link})")
else:
    st.info("Google Doc link not available yet")
