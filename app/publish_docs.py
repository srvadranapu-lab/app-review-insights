import os
from app.mcp_docs import append_to_doc, generate_doc_link

def publish_to_docs():
    """Publish report to Google Docs via MCP."""
    report_file = "data/report.txt"
    if not os.path.exists(report_file):
        print("Error: report.txt not found.")
        return None
    
    with open(report_file, 'r', encoding='utf-8') as f:
        report_content = f.read()
    
    product = "groww"
    week = "2026-W16"
    
    document_id = "1Ancm3RnEdYfVGgAdIBQu2imyIysAW8VkKD3378T6xP0"
    
    print("Appending report to document...")
    success = append_to_doc(document_id, report_content, week, product)
    
    if not success:
        print("Error: Failed to append to document.")
        return None
    
    doc_link = generate_doc_link(document_id)
    
    with open("data/doc_link.txt", 'w', encoding='utf-8') as f:
        f.write(doc_link)
    
    print(f"Document link: {doc_link}")
    return doc_link
