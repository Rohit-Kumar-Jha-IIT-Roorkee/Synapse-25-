from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from backend.generator import generate_ui_code
from backend.utils import extract_brand_colors
import shutil
import os
import traceback
import time

app = FastAPI()

# Allow frontend (like React) to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for now
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/generate")
async def generate_ui(
    prompt: str = Form(...),
    font: str = Form(...),
    format: str = Form("html"),  # html or jsx or shopify
    image: UploadFile = File(...)
):
    try:
        print("🟡 Step 1: Received request")

        # Step 2: Save image
        image_path = f"temp/{image.filename}"
        os.makedirs("temp", exist_ok=True)
        print("🟡 Step 2: Saving image at", image_path)

        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        print("🟢 Step 2: Image saved successfully")

        # Step 3: Extract brand colors
        print("🟡 Step 3: Extracting colors")
        brand_colors = extract_brand_colors(image_path)
        print("🟢 Step 3: Extracted colors:", brand_colors)

        # Step 4: Generate code
        print("🟡 Step 4: Generating UI code")
        code_dict = generate_ui_code(prompt, font, image_path)
        time.sleep(2)  # ⏳ Simulate delay of 2 seconds
        print("🟢 Step 4: UI code generated")

        return {
            "code": code_dict["code"],  # ✅ Return just the inner code dictionary
            "colors": brand_colors
        }

    except Exception as e:
        print("🔥 ERROR:", str(e))
        traceback.print_exc()
        return {"error": str(e)}
