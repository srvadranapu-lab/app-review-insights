import json
import os

def load_summary():
    """Load summary from data/summary.json."""
    summary_file = "data/summary.json"
    if not os.path.exists(summary_file):
        print("Error: summary.json not found. Run 'python -m app.cli summarize' first.")
        return None
    
    with open(summary_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_report(summary: dict, product: str = "Groww") -> str:
    """Generate a clean formatted one-page report."""
    themes = summary.get("themes", [])
    quotes = summary.get("quotes", [])
    actions = summary.get("actions", [])
    
    report = f"{product} — Weekly Review Pulse\n\n"
    report += "Top Themes\n"
    
    for theme in themes:
        report += f"- {theme}\n"
    
    report += "\nUser Quotes\n"
    for quote in quotes:
        report += f"- \"{quote}\"\n"
    
    report += "\nAction Ideas\n"
    for action in actions:
        report += f"- {action}\n"
    
    return report

def generate_email(summary: dict, product: str = "Groww") -> tuple[str, str]:
    """Generate email subject and HTML body."""
    themes = summary.get("themes", [])
    
    subject = f"Weekly Pulse — {product}"
    
    body = f"""<h3>Weekly Product Pulse</h3>

<b>Top Themes</b>
<ul>"""
    
    for theme in themes:
        body += f"<li>{theme}</li>"
    
    body += """</ul>

<a href="{DOC_LINK}">Read full report</a>"""
    
    return subject, body

def save_report(report: str, filepath: str = "data/report.txt"):
    """Save report to file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report)

def save_email(subject: str, body: str, filepath: str = "data/email.html"):
    """Save email to HTML file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"Subject: {subject}\n\n{body}")
