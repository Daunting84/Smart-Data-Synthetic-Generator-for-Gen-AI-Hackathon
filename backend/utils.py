# utils.py
import os
import time
selected_values = {}
session_state = {
    "generation_status": "idle",  # other values: "running", "ctgan_done", "privacy_done", "completed", "error"
    "output_path": None,
    "validation_results":None,
}


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

def collect_user_inputs(mode,input_path,user_intent=None):
    inputs = {}
    if mode =="data":
        inputs["input_path"] = input_path
        print("📦 collect_user_inputs received path:", input_path) 
        inputs["num_rows"] = selected_values.get("num_rows", 100)  # Default to 100 if missing
    elif mode =="prompt":
        inputs["custom_prompt"] = selected_values.get("custom_prompt", "")
        inputs["fields"] = selected_values.get("fields", [])
        inputs["use_case"] = selected_values.get("use_case", "general")  # default to 'general' if nothing set
        inputs["num_rows"] = selected_values.get("num_rows", 100)  # Default to 100 if missing

    elif mode =="both":
        inputs["input_path"] = input_path
        if user_intent =="modgen":
            inputs["custom_prompt"] = selected_values.get("custom_prompt", "")
            inputs["fields"] = selected_values.get("fields", [])
            inputs["use_case"] = selected_values.get("use_case", "general")  # default to 'general' if nothing set
            inputs["num_rows"] = selected_values.get("num_rows", 100)  # Default to 100 if missing
        elif user_intent =="genen":
            inputs["custom_prompt"] = selected_values.get("custom_prompt", "")
            inputs["fields"] = selected_values.get("fields", [])
            inputs["use_case"] = selected_values.get("use_case", "general")  # default to 'general' if nothing set
            inputs["num_rows"] = selected_values.get("num_rows", 100)  # Default to 100 if missing
        elif user_intent =="mod":
            inputs["custom_prompt"] = selected_values.get("custom_prompt", "")
            inputs["fields"] = selected_values.get("fields", [])
            inputs["use_case"] = selected_values.get("use_case", "general")  # default to 'general' if nothing set
    inputs["output_ext"] = selected_values.get("output_ext", "csv")
    return inputs

def save_dataframe(df, path):
    ext = os.path.splitext(path)[1].lower()
    os.makedirs(os.path.dirname(path), exist_ok=True)

    if ext == '.csv':
        df.to_csv(path, index=False)
    elif ext == '.json':
        df.to_json(path, orient='records', indent=2)
    elif ext in ['.xls', '.xlsx']:
        df.to_excel(path, index=False)
    else:
        raise ValueError(f"❌ Unsupported output file format: {ext}")