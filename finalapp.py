from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
from textSummarizer.pipeline.prediction import PredictionPipeline
# Assuming your PredictionPipeline is in this path
# from textSummarizer.pipeline.prediction import PredictionPipeline

app = FastAPI(
    title="Text Summarizer",
    description="A simple API and UI for summarizing text.",
    version="1.0"
)

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    This endpoint loads the main UI page.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict", response_class=HTMLResponse)
async def predict_route(request: Request, text: str = Form(...)):
    """
    This endpoint takes text from a form, generates a summary,
    and re-renders the page with the result.
    """
    try:
        obj = PredictionPipeline()
        summary = obj.predict(text)
        # Render the same template, but pass the results into it
        return templates.TemplateResponse("index.html", {
            "request": request,
            "summary": summary,
            "original_text": text
        })
    except Exception as e:
        # You might want to render an error on the page instead
        return templates.TemplateResponse("index.html", {
            "request": request,
            "error": str(e)
        })

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)