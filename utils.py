# utils.py
import os
import time

def get_output_path(filetype: str, model_choice: str) -> str:
    valid_exts = {".csv", ".json", ".xlsx"}
    filetype = filetype.strip().lower()

    if not filetype.startswith("."):
        filetype = f".{filetype}"

    if filetype not in valid_exts:
        print("⚠️ Invalid or missing extension. Defaulting to .csv")
        filetype = ".csv"

    os.makedirs("output", exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"synthetic_output_{model_choice}_{timestamp}{filetype}"
    return os.path.join("output", filename)

def collect_user_inputs(mode):
    inputs = {}
    if mode in ["data", "both"]:
        inputs["input_path"] = input("Enter path to your CSV, JSON, or Excel file: ").strip()
    if mode in ["prompt", "both"]:
        inputs["custom_prompt"] = input("Describe the format or style of text data you'd like: ")
        inputs["fields"] = [f.strip() for f in input("Enter comma-separated column names: ").split(",") if f.strip()]
        inputs["use_case"] = input("Pick a use case (e.g., chat messages, login attempts, patient records): ").strip()
    inputs["output_ext"] = input("Choose output file type (csv/json/xlsx): ").strip()
    inputs["num_rows"] = int(input("How many rows of synthetic data? "))
    return inputs