import os
import time
import joblib
import pandas as pd
import json
from dotenv import load_dotenv

from schema_profiler import load_dataframe, profile_schema
from model_dispatcher import decide_model
from ctgan_generator import generate_synthetic_data
from text_generator import generate_text_data

# Ensure parallel processing doesn't crash
os.environ["JOBLIB_MULTIPROCESSING"] = "0"
joblib.parallel.DEFAULT_N_JOBS = 1

# Load .env variables
load_dotenv()

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

def main():
    model_choice = input("Which model do you want to use? (ctgan/textgen): ").strip().lower()

    if model_choice == "ctgan":
        input_path = input("Enter path to your CSV, JSON, or Excel file: ").strip()
        output_ext = input("Choose file type for output (csv/json/xlsx): ").strip()
        output_path = get_output_path(output_ext, model_choice)

        df = load_dataframe(input_path)
        df = df.sample(min(len(df), 3000), random_state=42)

        num_rows = int(input("How many rows of synthetic data do you want to generate? "))

        schema = profile_schema(df)
        model_type = decide_model(schema)
        print(f"Model selected: {model_type}")
        print(json.dumps(schema, indent=2, default=str))

        if model_type == "ctgan":
            discrete_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
            generate_synthetic_data(input_path, output_path, df, num_rows, discrete_cols)

    elif model_choice == "textgen":
        output_ext = input("Choose file type for output (csv/json/xlsx): ").strip()
        output_path = get_output_path(output_ext, model_choice)

        custom_prompt = input("Describe the format or style of text data you'd like: ")
        num_rows = int(input("How many rows of synthetic text data? "))

        fields_raw = input("Enter comma-separated column names (e.g., name, dob, age): ").strip()
        fields = [f.strip() for f in fields_raw.split(",") if f.strip()]
        if not fields:
            print("❌ You must provide at least one column name.")
            return

        use_case = input("Pick a use case (e.g., chat messages/structured text records/feedback forms/transaction records/inventory logs/login attempts/human records): ").strip()

        few_shot = ",".join(fields) + "\n" + ",".join(["Example"] * len(fields))
        df = pd.DataFrame([x.split(",") for x in few_shot.split("\n")[1:]], columns=fields)
        schema = profile_schema(df)

        generate_text_data(schema, fields, use_case, few_shot, custom_prompt, num_rows=num_rows, output_path=output_path)

    else:
        print("❌ Unknown model type.")

if __name__ == "__main__":
    main()
