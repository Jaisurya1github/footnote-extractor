from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import os, uuid
from extract import extract_footnotes

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

app = FastAPI(title="XML Footnote Extractor")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/upload")
async def upload_xml(file: UploadFile = File(...)):
    job_id = str(uuid.uuid4())

    input_path = f"{UPLOAD_DIR}/{job_id}.xml"
    output_path = f"{OUTPUT_DIR}/{job_id}_footnotes.xml"

    with open(input_path, "wb") as f:
        while chunk := await file.read(1024 * 1024):
            f.write(chunk)

    extract_footnotes(input_path, output_path)

    return FileResponse(
        path=output_path,
        filename="footnotes.xml",
        media_type="application/xml"
    )
