from fastapi import APIRouter, HTTPException, FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .gpt import generate_campaign_emails
from .models import CampaignResponse, Account
from typing import List
from pydantic import BaseModel
from pathlib import Path
from fastapi import Request
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Input Models
class Contact(BaseModel):
    name: str
    email: str
    job_title: str

class CampaignRequest(BaseModel):
    accounts: List[Account]
    number_of_emails: int

# FastAPI Setup
app = FastAPI()
router = APIRouter()

# Mount the static directory
app.mount("/static", StaticFiles(directory=Path(__file__).parent.parent / "static"), name="static")

# Set up templates
templates = Jinja2Templates(directory=Path(__file__).parent.parent / "static")

@router.post("/generate-campaign/", response_model=List[CampaignResponse])
async def create_campaign(request: CampaignRequest):
    try:
        campaigns = await generate_campaign_emails(request)
        return campaigns
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

app.include_router(router)
