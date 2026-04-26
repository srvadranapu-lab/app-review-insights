import requests

MCP_BASE_URL = "https://saksham-mcp-server-rufx.onrender.com"

def send_email(subject: str, html_body: str, to_email: str = "your_email@gmail.com"):
    """Send email via Gmail MCP."""
    url = f"{MCP_BASE_URL}/create_email_draft"
    
    payload = {
        "to": to_email,
        "subject": subject,
        "body": html_body  # Note: MCP expects "body" not "html"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
