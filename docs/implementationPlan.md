Weekly Product Review Pulse — Implementation Plan
This implementation follows a phase-wise approach aligned with the architecture.
Each phase is independently testable, prompt-driven (Windsurf), and demoable.
 
Guiding Principles
•	Build in vertical slices (each phase runnable) 
•	Maintain strict MCP boundary (only Phase 5 & 6) 
•	Ensure idempotency from Phase 0 
•	Use free-tier tools only 
•	Avoid unnecessary complexity (no embeddings) 
 
Phase Overview (table)
Phase	Name	Outcome
0	Foundations	Project + CLI + DB ready
1	Ingestion	Reviews collected & stored
2	Processing	Cleaned dataset
3	Summarization	Insights generated
4	Rendering	Report + Email artifacts
5	Docs MCP	Report appended to Google Docs
6	Gmail MCP	Email sent
7	Orchestration	Full pipeline automated
 
Phase 0 — Foundations
Goal
Set up project structure, configuration, database, and CLI.
Scope
•	Create project structure 
•	Setup FastAPI backend 
•	Setup SQLite database 
•	Define schemas 
•	CLI (pulse) setup 
•	Environment configuration 
•	Logging setup 
Output
•	CLI runs 
•	Database initializes 
•	Project compiles 
Exit Criteria
•	pulse --help works 
•	DB tables created successfully 
•	Config loads correctly 
 
Phase 1 — Review Ingestion
Goal
Fetch and store reviews from App Store and Play Store.
Scope
•	App Store RSS ingestion 
•	Play Store ingestion 
•	Normalize schema 
•	Deduplicate reviews 
•	PII scrubbing 
•	Store in SQLite 
Output
•	Reviews stored in DB 
Exit Criteria
•	≥200 reviews fetched (live test) 
•	Re-run does not duplicate data 
•	Data stored correctly 
 
Phase 2 — Processing & Cleaning
Goal
Prepare dataset for LLM processing.
Scope
•	Filter English reviews 
•	Remove short/low-quality reviews 
•	Prepare structured input 
•	Limit dataset size for LLM efficiency 
Output
•	Clean dataset ready for summarization 
Exit Criteria
•	Only valid reviews passed forward 
•	Dataset stable across runs 
 
Phase 3 — LLM Summarization
Goal
Generate themes, quotes, and action ideas using LLM.
Scope
•	Use Groq 
•	Generate: 
o	Top 3 themes 
o	3 quotes (validated) 
o	3 action ideas 
•	Enforce structured JSON output 
•	Validate quotes against review text 
Output
•	PulseSummary JSON 
Exit Criteria
•	Output ≤250 words 
•	All quotes are real (validated) 
•	JSON structure is correct 
 
Phase 4 — Report & Email Rendering
Goal
Convert summary into report and email formats.
Scope
•	Generate one-page report 
•	Generate email draft (HTML + text) 
•	Insert placeholders for Doc link 
Output
•	Report file 
•	Email draft 
Exit Criteria
•	Output is readable and structured 
•	Email contains correct summary 
 
Phase 5 — Google Docs MCP Integration
Goal
Append report to Google Docs using MCP.
Scope
•	Connect to MCP server 
•	Locate or create product document 
•	Append new section with anchor:
pulse-{product}-{week}
•	Retrieve heading ID 
•	Generate deep link 
Output
•	Report appended to Google Doc 
•	Deep link generated 
Exit Criteria
•	First run creates section 
•	Second run does not duplicate 
•	Deep link works 
 
Phase 6 — Gmail MCP Integration
Goal
Send stakeholder email via MCP.
Scope
•	Create email draft 
•	Insert deep link 
•	Add idempotency header:
X-Pulse-Run-Id
•	Send email (controlled by flag) 
Output
•	Email sent or draft created 
Exit Criteria
•	Email sent once per run 
•	Re-run does not resend 
•	Message ID stored 
 
Phase 7 — Orchestration & Automation
Goal
Run entire pipeline automatically.
Scope
•	Combine all phases into single command 
•	Add run tracking 
•	Schedule weekly execution 
•	Add logging and monitoring 
Output
•	Fully automated pipeline 
Exit Criteria
•	End-to-end run successful 
•	No duplicate outputs 
•	Logs available for debugging 
 
Data Flow Summary
Ingestion → Processing → LLM → Rendering → MCP Docs → MCP Gmail
 
Idempotency Strategy
•	Run ID:
sha1(product + week)
•	Docs: 
o	Anchor check prevents duplicates 
•	Email: 
o	Header check prevents duplicates 
 
Deliverables per Phase (table)
Phase	Deliverable
0	Project scaffold
1	Reviews dataset
2	Clean dataset
3	Insights JSON
4	Report + Email
5	Google Doc update
6	Email sent
7	Automated system
 
Success Criteria
•	Weekly report generated automatically 
•	Themes reflect real user issues 
•	Quotes are verbatim 
•	Actions are actionable 
•	Google Doc maintains history 
•	Email links to correct section