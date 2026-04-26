Architecture
1. Overview
This system is an AI agent that ingests public App Store and Google Play reviews for selected fintech products and generates a weekly one-page insight report.
The report is delivered using MCP (Model Context Protocol):
•	Appended to a running Google Doc (system of record) 
•	Sent via Gmail as a short email with a deep link to the report 
The agent does not directly call Google APIs. All interactions with Google Docs and Gmail happen strictly through MCP servers.
 
2. Objectives
•	Generate a weekly product review pulse automatically 
•	Extract: 
o	Top themes (max 5) 
o	Real user quotes (validated) 
o	3 action ideas 
•	Deliver outputs via: 
o	Google Docs (append-only history) 
o	Gmail (stakeholder notification) 
•	Ensure: 
o	Idempotency (no duplicate runs) 
o	Auditability (track every run) 
o	Low cost (free-tier optimized) 
 
3. System Architecture
High-Level Flow
App Store + Play Store
        ↓
   Ingestion Layer
        ↓
   Processing Layer
        ↓
   LLM (Groq)
        ↓
   Report Generator
        ↓
   MCP Layer
   ↙        ↘
Google Docs   Gmail
 
4. Core Components
4.1 Ingestion Layer
Responsible for collecting reviews from public sources.
Sources:
•	App Store (iTunes RSS feed) 
•	Play Store (google-play-scraper) 
Responsibilities:
•	Fetch last 8–12 weeks of reviews 
•	Normalize into a unified schema 
•	Deduplicate reviews 
•	Scrub PII (emails, phone numbers) 
•	Store in SQLite 
 
4.2 Processing Layer
Prepares data for insight generation.
Responsibilities:
•	Filter: 
o	English-only reviews 
o	Minimum length threshold 
•	Structure reviews for LLM input 
•	No embeddings used (to reduce cost and complexity) 
 
4.3 LLM Layer (Groq)
Uses Groq for all reasoning.
Responsibilities:
•	Group reviews into ≤5 themes 
•	Generate: 
o	Top 3 themes 
o	3 validated user quotes 
o	3 action ideas 
Constraints:
•	Output ≤250 words 
•	Quotes must match actual review text (validated post-generation) 
•	Strict JSON output format 
 
4.4 Report Generator
Converts structured insights into human-readable outputs.
Outputs:
1.	Weekly Report (one-page) 
2.	Email Draft (HTML + text) 
Structure:
•	Product name + time window 
•	Top themes 
•	User quotes 
•	Action ideas 
•	“Who this helps” section 
 
4.5 MCP Layer (Google Workspace Integration)
The agent connects to two MCP servers:
Google Docs MCP
Purpose:
•	Append weekly report to a running document 
Behavior:
•	One document per product 
•	Each run adds a new section:
Weekly Pulse — {Product} — {ISO Week}
•	Uses anchor:
pulse-{product}-{week}
•	Prevents duplicate inserts 
Output:
•	docId 
•	headingId 
•	Deep link:
https://docs.google.com/document/d/{docId}/edit#heading={headingId}
 
Gmail MCP
Purpose:
•	Send stakeholder email 
Behavior:
•	Creates email draft first 
•	Sends only if enabled 
•	Includes deep link to Google Doc section 
•	Uses idempotency header:
X-Pulse-Run-Id
Output:
•	messageId 
 
5. Data Model
RawReview
id: string
product: string
source: appstore | playstore
rating: int
title: string
body: string
date: datetime
 
PulseSummary
product: string
window: date range
top_themes: list
quotes: list
action_ideas: list
 
Run Metadata
run_id: string
product: string
week: string
doc_heading_id: string
email_message_id: string
status: string
 
6. Idempotency
Run ID
run_id = sha1(product + iso_week)
 
Docs Idempotency
•	Search for anchor:
pulse-{product}-{week}
•	If exists → skip append 
 
Email Idempotency
•	Search Gmail using:
X-Pulse-Run-Id
•	If exists → skip send 
 
7. Storage
Uses SQLite (local, lightweight)
Tables:
•	reviews 
•	runs 
•	summaries 
Google Doc acts as the long-term human-readable record
 
8. Security & Safety
•	PII removed before: 
o	LLM processing 
o	Report generation 
•	Reviews treated as data (not instructions) 
•	No Google credentials stored in agent 
•	Credentials handled only inside MCP servers 
 
9. Deployment Architecture
Backend
•	Deployed on Render 
MCP Server
•	Deployed separately on Render 
•	Handles: 
o	Google Docs 
o	Gmail 
Execution
•	Weekly scheduled run (cron) 
 
10. Key Design Decisions
•	No embeddings → reduces cost and complexity 
•	Groq LLM → fastest free inference 
•	SQLite → no external DB dependency 
•	MCP-only Google integration → secure and modular 
•	Append-only Docs → preserves history 
 
11. End-to-End Flow
1. Fetch reviews
2. Clean + filter
3. Send to Groq LLM
4. Generate insights
5. Format report
6. Append to Google Docs via MCP
7. Send email via Gmail MCP
 
12. Success Criteria
•	One-page weekly pulse generated 
•	Quotes are real and validated 
•	No duplicate Doc sections 
•	No duplicate emails 
•	Fully automated weekly execution 