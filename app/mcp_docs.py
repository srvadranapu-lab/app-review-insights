import requests
import json

MCP_BASE_URL = "https://saksham-mcp-server-rufx.onrender.com"

def get_available_tools():
    """Get available tools from MCP server."""
    url = f"{MCP_BASE_URL}/tools"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error getting tools: {e}")
        return {}

def append_to_doc(doc_id: str, content: str, week: str, product: str = "groww"):
    """Append content to Google Doc via MCP."""
    url = f"{MCP_BASE_URL}/append_to_doc"
    
    # Create anchor and format content
    anchor = f"pulse-{product}-{week}"
    formatted_content = f"Weekly Pulse — {product.title()} — {week}\n\n{content}\n\n---"
    
    payload = {
        "doc_id": doc_id,
        "content": formatted_content
    }
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error appending to document: {e}")
        return False

def generate_doc_link(doc_id: str) -> str:
    """Generate Google Doc link."""
    return f"https://docs.google.com/document/d/{doc_id}"
