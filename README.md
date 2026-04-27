# 📊 App Review Insights Analyser

## 🔗 Live Demo
https://app-review-insights.onrender.com/

---

## 🚀 Overview

App Review Insights Analyser is an AI-powered tool that converts raw App Store and Google Play reviews into a **one-page weekly product pulse**.

It helps:
- **Product teams** prioritize what to fix
- **Support teams** understand user complaints
- **Leadership** get a quick health snapshot

---

## ⚙️ What It Does

- Ingests app reviews (last 8–12 weeks)
- Cleans and filters data
- Uses LLM (Groq) to extract:
  - Top themes
  - Real user quotes (validated)
  - 3 actionable insights
- Generates:
  - 📄 Weekly report
  - 📧 Email draft (Gmail-ready)
- Publishes report to Google Docs

---

## 🧠 Tech Stack

- **IDE:** Windsurf  
- **Backend:** Python  
- **UI:** Streamlit  
- **LLM:** Groq (free-tier optimized)  
- **Database:** SQLite  
- **Deployment:** Render  
- **Integrations:** Google Docs + Gmail (via MCP-style server)

---

## 🛠️ How to Use

1. Click **Run Ingestion**  
2. Click **Process Reviews**  
3. Click **Generate Insights**  
4. Click **Generate Report**  
5. Click **Publish to Google Docs**  
6. Click **Send Email**

---

## 📦 Output

### 📄 Weekly Report
- Top 3 themes
- Real user quotes
- Actionable product ideas

### 📧 Email Draft
- Opens directly in Gmail
- Pre-filled subject + body
- Includes Google Doc link

---

## 📁 Project Structure
app/
├── ingestion.py
├── processing.py
├── summarize.py
├── render.py
├── publish_docs.py
├── publish_email.py
├── ui.py
├── database.py
docs/
data/

---

## ⚠️ Constraints Followed

- No PII included
- Max 5 themes (top 3 shown)
- ≤250 words report
- Public review data only
- Free-tier tools only

---

## ✅ Key Features

- End-to-end automated pipeline
- Clean UI for execution
- Real user quotes (validated)
- Google Docs integration
- Gmail-ready email flow
- Fully deployable prototype

---

## 🎯 Future Improvements

- Multi-product support
- Better theme clustering
- Scheduled weekly automation
- Improved UI/UX

---

## 👤 Author

Sai Ram Vadranapu
