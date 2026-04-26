import os
import re
from urllib.parse import quote

def strip_html_tags(html):
    """Basic HTML tag stripping."""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html)

def publish_email():
    """Generate Gmail compose URL for email."""
    # Load email HTML
    email_file = "data/email.html"
    if not os.path.exists(email_file):
        print("Error: email.html not found. Run 'python -m app.cli render' first.")
        return None
    
    with open(email_file, 'r', encoding='utf-8') as f:
        email_content = f.read()
    
    # Load doc link
    doc_link_file = "data/doc_link.txt"
    if not os.path.exists(doc_link_file):
        print("Error: doc_link.txt not found. Run 'python -m app.cli publish_docs' first.")
        return None
    
    with open(doc_link_file, 'r', encoding='utf-8') as f:
        doc_link = f.read().strip()
    
    # Replace DOC_LINK placeholder
    email_content = email_content.replace("{DOC_LINK}", doc_link)
    
    # Extract subject and body
    lines = email_content.split('\n')
    subject = "Weekly Pulse — Groww"
    
    # Find HTML body (skip subject line if present)
    html_body = email_content
    if lines and lines[0].startswith("Subject:"):
        html_body = '\n'.join(lines[2:])  # Skip subject and empty line
    
    # Convert HTML to plain text
    plain_text = strip_html_tags(html_body)
    
    # Create Gmail compose URL
    encoded_subject = quote(subject)
    encoded_body = quote(plain_text)
    
    gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to=&su={encoded_subject}&body={encoded_body}"
    
    print(f"Gmail compose URL generated: {gmail_url}")
    return gmail_url
