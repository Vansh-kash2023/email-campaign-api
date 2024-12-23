from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.models import InputData, SuccessResponse, ErrorResponse
from app.services import generate_email_campaign

app = FastAPI(
    title="Personalized Email Drip Campaign API",
    description="API for generating personalized email sequences for ABM campaigns",
    version="1.0.0"
)

# Set up templates directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Serve the landing page with details about the API.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate_campaign", response_model=SuccessResponse, responses={400: {"model": ErrorResponse}})
async def generate_campaign(data: InputData):
    """
    Generate a personalized email drip campaign based on the input account data.
    """
    try:
        result = await generate_email_campaign(data)
        return {"campaigns": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
