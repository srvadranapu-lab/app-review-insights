import os
import re
from urllib.parse import quote

def strip_html_tags(html):
    """Basic HTML tag stripping."""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html)

def publish_email():
    """Generate Gmail compose URL for email."""
    
    email_file = "data/email.html"
    if not os.path.exists(email_file):
        print("Error: email.html not found.")
        return None
    
    with open(email_file, 'r', encoding='utf-8') as f:
        email_content = f.read()
    
    # Load doc link (optional but important)
    doc_link = ""
    doc_link_file = "data/doc_link.txt"
    if os.path.exists(doc_link_file):
        with open(doc_link_file, 'r', encoding='utf-8') as f:
            doc_link = f.read().strip()
    
    # Inject doc link if placeholder exists
    if "{DOC_LINK}" in email_content:
        email_content = email_content.replace("{DOC_LINK}", doc_link)
    
    # Subject
    subject = "Weekly Pulse — Groww"
    
    # Convert HTML → readable plain text
    plain_text = strip_html_tags(email_content)
    
    # Add doc link at bottom (CRITICAL UX FIX)
    if doc_link:
        plain_text += f"\n\nRead full report: {doc_link}"
    
    # Encode
    encoded_subject = quote(subject)
    encoded_body = quote(plain_text)
    
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&su={encoded_subject}&body={encoded_body}"
    
    return gmail_url
