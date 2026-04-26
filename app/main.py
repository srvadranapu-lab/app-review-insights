from fastapi import FastAPI
from app.database import db

app = FastAPI(title="App Review Insights Analyser")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.on_event("startup")
async def startup_event():
    # Initialize database on startup
    db.init_db()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
