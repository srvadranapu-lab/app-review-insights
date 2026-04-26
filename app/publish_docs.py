import os
from app.mcp_docs import append_to_doc, generate_doc_link, get_available_tools

def publish_to_docs():
    """Publish report to Google Docs via MCP."""
    # Load report
    report_file = "data/report.txt"
    if not os.path.exists(report_file):
        print("Error: report.txt not found. Run 'python -m app.cli render' first.")
        return
    
    with open(report_file, 'r', encoding='utf-8') as f:
        report_content = f.read()
    
    # Configuration
    product = "groww"
    week = "2026-W16"  # Hardcoded for now
    # Hardcoded document ID for demo - in production this would be created/stored
    document_id = "1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms"  # Example Google Doc ID
    
    print(f"Checking MCP server tools...")
    tools = get_available_tools()
    print(f"Available tools: {[tool.get('name') for tool in tools] if tools else 'None'}")
    
    print(f"Appending report to document...")
    success = append_to_doc(document_id, report_content, week, product)
    
    if not success:
        print("Error: Failed to append to document.")
        return
    
    # Generate and save link
    doc_link = generate_doc_link(document_id)
    
    link_file = "data/doc_link.txt"
    with open(link_file, 'w', encoding='utf-8') as f:
        f.write(doc_link)
    
    print(f"Document link: {doc_link}")
    print(f"Link saved to {link_file}")
    return doc_link
