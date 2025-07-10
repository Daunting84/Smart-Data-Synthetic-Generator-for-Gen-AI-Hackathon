### main.py
import os
import time
import joblib
import shutil
import pandas as pd
import json
from dotenv import load_dotenv
import uuid
from datetime import datetime
from utils import session_state

from schema_profiler import load_dataframe, profile_schema
from model_dispatcher import decide_model
from utils import get_output_path, collect_user_inputs
from utils import selected_values
from utils import session_state
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List


save_dir = "inputs"
os.makedirs(save_dir, exist_ok=True) 

app = FastAPI()


# Allow your React frontend to talk to FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # or "*" during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ModeSelection(BaseModel):
    mode: str

@app.post("/set-mode")
async def set_mode(selection: ModeSelection):
    selected_values["mode"] = selection.mode.strip().lower()
    print("Mode set to:", selected_values["mode"])
    return {"message": f"Mode set to {selected_values['mode']}"}

class DualModeSelection(BaseModel):
    user_intent: str

@app.post("/set-dual-mode")
async def set_dual_mode(selection: DualModeSelection):
    selected_values["dual_mode"] = selection.user_intent.strip().lower()
    print("Dual Mode set to:", selected_values["dual_mode"])
    return {"message": f"Mode set to {selected_values['dual_mode']}"}

@app.post("/upload-file/")
async def upload_file(file: UploadFile = File(...)):
    try:
        allowed_ext = ['.csv', '.json', '.xlsx']
        ext = os.path.splitext(file.filename)[1].lower()
        if ext not in allowed_ext:
            raise HTTPException(status_code=400, detail="Invalid file extension")

        filename = file.filename  # ← leave filename unchanged
        os.makedirs("inputs", exist_ok=True)
        save_path = os.path.abspath(os.path.join("inputs", filename))

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        selected_values["input_path"] = save_path
        print("✅ File saved at:", save_path)

        return {"filename": filename, "filepath": save_path}
    except Exception as e:
        print("❌ Upload error:", str(e))
        raise HTTPException(status_code=500, detail="Upload failed")
class PromptInput(BaseModel):
    custom_prompt: str

@app.post("/set-prompt")
async def set_prompt(prompt_data: PromptInput):
    # Store this globally or however you're managing session state
    selected_values["custom_prompt"] = prompt_data.custom_prompt.strip()
    print("Prompt received:", selected_values["custom_prompt"])
    return {"message": "Prompt received successfully"}

class UseCaseInput(BaseModel):
    use_case: str

@app.post("/set-use-case")
async def set_use_case(data: UseCaseInput):
    selected_values["use_case"] = data.use_case.strip()
    print("Use case set to:", selected_values["use_case"])
    return {"message": f"Use case '{data.use_case}' received"}

class FieldInput(BaseModel):
    fields: List[str]

@app.post("/set-fields")
async def set_fields(data: FieldInput):
    selected_values["fields"] = [f.strip() for f in data.fields if f.strip()]
    print("Fields set to:", selected_values["fields"])
    return {"message": f"{len(selected_values['fields'])} fields received"}

class RowCountInput(BaseModel):
    num_rows: int

@app.post("/set-rows")
async def set_num_rows(data: RowCountInput):
    if data.num_rows <= 0:
        raise HTTPException(status_code=400, detail="Number of rows must be a positive integer.")
    selected_values["num_rows"] = data.num_rows
    print("Rows set to:", data.num_rows)
    return {"message": f"{data.num_rows} rows requested"}

class OutputFormat(BaseModel):
    output_ext: str

@app.post("/set-output-format")
async def set_output_format(data: OutputFormat):
    ext = data.output_ext.strip().lower()
    if ext not in ["csv", "json", "xlsx"]:
        raise HTTPException(status_code=400, detail="Invalid output format")
    
    selected_values["output_ext"] = ext
    print("Output format set to:", ext)
    return {"message": f"Output format set to {ext}"}

class PrivacySettings(BaseModel):
    noise_stddev: float
    category_swap_fraction: float
    masked_columns: list[str]

@app.post("/set-privacy")
async def set_privacy(settings: PrivacySettings):
    selected_values["privacy"] = {
        "noise_stddev": settings.noise_stddev / 100,
        "category_swap_fraction": settings.category_swap_fraction / 100,
        "masked_columns": settings.masked_columns
    }
    print("Saved privacy settings:", selected_values["privacy"])
    return {"message": "Privacy settings saved."}

@app.post("/generate-data")
async def generate_data():
    try:
        save_path = selected_values.get("input_path")
        main(save_path)
        return {"status": "success", "message": "Data generated"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
       


@app.get("/check-output")
def check_output_ready():
    output_path = session_state.get("output_path")
    if output_path and os.path.exists(output_path):
        return JSONResponse(content={"ready": True})
    return JSONResponse(content={"ready": False})

@app.get("/generation-status")
def get_generation_status():
    return {
        "status": session_state.get("generation_status", "idle"),
        "output_path": session_state.get("output_path")
    }

@app.get("/download-output")
def download_output():
    output_path = session_state.get("output_path")
    if not output_path or not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail="No output file found.")
    
    return FileResponse(
        output_path,
        media_type="application/octet-stream",
        filename=os.path.basename(output_path)
    )

@app.get("/get-validation-results")
def get_validation_results():
    results = session_state.get("validation_results")
    if results is None:
        return {"message": "Validation not applicable for this mode."}
    if not results:
        raise HTTPException(status_code=404, detail="No validation results available yet.")
    return results

# Ensure parallel processing doesn't crash
os.environ["JOBLIB_MULTIPROCESSING"] = "0"
joblib.parallel.DEFAULT_N_JOBS = 1

# Load .env variables
load_dotenv()

def main(save_path):
    print("📁 save_path received:", save_path)

    session_state["generation_status"] = "in main"

    mode = selected_values.get("mode")
    session_state["generation_status"] = "got mode"
    user_intent = None
    if not mode:
        raise Exception("Mode not set — please set it from frontend first.")
    if mode not in ["data", "prompt", "both"]:
        print("❌ Invalid mode selected.")
        exit(1)
    if mode=="both":
        session_state["generation_status"] = "in both"
        user_intent = selected_values.get("dual_mode", None)
        print("Received mode:", mode)
        print("Received dual_mode intent:", user_intent)
        if not user_intent:
            raise Exception("Dual Mode not set — please set it from frontend first.")
        if user_intent not in ["modgen", "genen", "mod"]:
            session_state["generation_status"] = "not in error"
            print("❌ Invalid combo-mode selected.")
            exit(1)
    session_state["generation_status"] = "out"
    user_inputs = collect_user_inputs(mode,input_path=save_path,user_intent=user_intent)
    decide_model(mode, user_inputs,user_intent=user_intent)
    print("✅ Main finished running — ready to return response")
    session_state["generation_status"] = "completed"

if __name__ == "__main__":
    main()