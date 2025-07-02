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

def collect_user_inputs(mode,user_intent=None):
    inputs = {}
    if mode =="data":
        inputs["input_path"] = input("Enter path to your CSV, JSON, or Excel file: ").strip()
    elif mode =="prompt":
        inputs["custom_prompt"] = input("Describe the format or style of text data you'd like: ")
        inputs["fields"] = [f.strip() for f in input("Enter comma-separated column names: ").split(",") if f.strip()]
        inputs["use_case"] = input("Pick a use case (e.g., chat messages, login attempts, patient records): ").strip()
    elif mode =="both":
        inputs["input_path"] = input("Enter path to your CSV, JSON, or Excel file: ").strip()
        if user_intent =="modgen":
            inputs["custom_prompt"] = input("Describe the modifications you would like to make to the data: ")
            inputs["fields"] = [f.strip() for f in input("Enter comma-separated column names: ").split(",") if f.strip()]
            inputs["use_case"] = input("Pick a use case (e.g., chat messages, login attempts, patient records): ").strip()
        elif user_intent =="genen":
            inputs["custom_prompt"] = input("Describe how you would like to fine tune your data after generation: ")
            inputs["fields"] = [f.strip() for f in input("Enter comma-separated column names: ").split(",") if f.strip()]
            inputs["use_case"] = input("Pick a use case (e.g., chat messages, login attempts, patient records): ").strip()
        elif user_intent =="mod":
            inputs["custom_prompt"] = input("Describe how you would like your data to be modified: ")
            inputs["fields"] = [f.strip() for f in input("Enter comma-separated column names: ").split(",") if f.strip()]
            inputs["use_case"] = input("Pick a use case (e.g., chat messages, login attempts, patient records): ").strip()
    inputs["output_ext"] = input("Choose output file type (csv/json/xlsx): ").strip()
    inputs["num_rows"] = int(input("How many rows of synthetic data? "))
    return inputs
