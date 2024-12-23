import os
import logging
from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models import InputData, SuccessResponse, ErrorResponse
from app.services import generate_email_campaign

if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename='logs/error.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="Personalized Email Drip Campaign API",
    description="API for generating personalized email sequences for ABM campaigns",
    version="1.0.0"
)

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        logging.error(f"Error rendering template at '/': {str(e)}")
        raise HTTPException(status_code=500, detail="Error rendering template")

@app.post("/generate_campaign", response_model=SuccessResponse, responses={400: {"model": ErrorResponse}})
async def generate_campaign(data: InputData):
    try:
        result = await generate_email_campaign(data)
        return {"campaigns": result}
    except Exception as e:
        logging.error(f"Error generating campaign: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
