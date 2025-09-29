from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from db import init_db, SessionLocal, EmailLog
from classifier import classify_email, detect_intents
from background import run_in_background
from pydantic import BaseModel

app = FastAPI()

# Setup templates
templates = Jinja2Templates(directory="templates")

class EmailRequest(BaseModel):
    subject: str
    body: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    init_db()
    run_in_background()

@app.post("/classify")
def classify_email_endpoint(email: EmailRequest):
    text = email.subject + " " + email.body
    predictions = classify_email(text)
    intents = detect_intents(predictions)
    return {"predictions": predictions, "intents": intents}

# ✅ Frontend dashboard
@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    emails = db.query(EmailLog).order_by(EmailLog.created_at.desc()).limit(20).all()

    # Ensure predictions are in a uniform format for the template
    for email in emails:
        if email.predictions:
            # Convert list of dicts or objects to a uniform list of objects with .intent and .score
            formatted = []
            for p in email.predictions:
                if isinstance(p, dict):
                    formatted.append(type('Prediction', (), {'intent': p.get('intent'), 'score': p.get('score')})())
                elif isinstance(p, (list, tuple)) and len(p) == 2:
                    formatted.append(type('Prediction', (), {'intent': p[0], 'score': p[1]})())
                else:
                    formatted.append(p)  # assume already has .intent and .score
            email.predictions = formatted
        else:
            email.predictions = []

    return templates.TemplateResponse("dashboard.html", {"request": request, "emails": emails})
