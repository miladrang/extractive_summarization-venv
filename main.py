# Import libraries and modules
##############################
from app import text_summarization
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


# To create instance from FastApi
fapi = FastAPI()
fapi.mount("/static", StaticFiles(directory="static"), name="static")


# To use the html file to display the input form on the main page
@fapi.get("/", response_class=HTMLResponse)
async def home():
    with open("static/form.html", "r") as f:
        form_html = f.read()
    return form_html


# To process the input text sent from the form
@fapi.post("/summarize")
async def summarize(text_input: str = Form(...)):
    summary = text_summarization(text_input)
    summary = " ".join(summary)
    return f"Your summarized text: {summary}"
