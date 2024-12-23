import os
import logging
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

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate_campaign", response_model=SuccessResponse, responses={400: {"model": ErrorResponse}})
async def generate_campaign(data: InputData):
    try:
        result = await generate_email_campaign(data)
        return {"campaigns": result}
    except Exception as e:
        logging.error(f"Error generating campaign: {str(e)}")
        raise HTTPException(status_code=400, detail={str(e)})

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    logging.info(f"Starting server on 0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
