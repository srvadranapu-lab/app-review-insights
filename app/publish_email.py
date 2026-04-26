import os
from app.mcp_gmail import send_email

def publish_email():
    """Publish email via Gmail MCP."""
    # Load email HTML
    email_file = "data/email.html"
    if not os.path.exists(email_file):
        print("Error: email.html not found. Run 'python -m app.cli render' first.")
        return
    
    with open(email_file, 'r', encoding='utf-8') as f:
        email_content = f.read()
    
    # Load doc link
    doc_link_file = "data/doc_link.txt"
    if not os.path.exists(doc_link_file):
        print("Error: doc_link.txt not found. Run 'python -m app.cli publish_docs' first.")
        return
    
    with open(doc_link_file, 'r', encoding='utf-8') as f:
        doc_link = f.read().strip()
    
    # Replace DOC_LINK placeholder
    email_content = email_content.replace("{DOC_LINK}", doc_link)
    
    # Extract subject (first line) and body (rest)
    lines = email_content.split('\n')
    subject = "Weekly Pulse — Groww"  # Fixed subject as requested
    
    # Find HTML body (skip subject line if present)
    html_body = email_content
    if lines and lines[0].startswith("Subject:"):
        html_body = '\n'.join(lines[2:])  # Skip subject and empty line
    
    print(f"Sending email...")
    success = send_email(subject, html_body)
    
    if success:
        print("Email sent successfully!")
        print(f"Subject: {subject}")
        print(f"Doc link: {doc_link}")
    else:
        print("Error: Failed to send email.")
    
    return success
