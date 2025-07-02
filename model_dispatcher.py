import os
import json
import time
import pandas as pd
import joblib
from dotenv import load_dotenv

from schema_profiler import load_dataframe, profile_schema
from ctgan_generator import generate_synthetic_data
from text_generator import generate_text_data
from combo_generator import generate_combo_data
from utils import get_output_path, collect_user_inputs

# Safety for parallel backend
os.environ["JOBLIB_MULTIPROCESSING"] = "0"
joblib.parallel.DEFAULT_N_JOBS = 1

load_dotenv()

def decide_model(mode):
    # Prompt only ONCE if mode is not "both"
    if mode in ["data", "prompt"]:
        user_inputs = collect_user_inputs(mode)

    if mode == "data":
        input_path = user_inputs["input_path"]
        output_path = get_output_path(user_inputs["output_ext"], "ctgan")

        df = load_dataframe(input_path)
        df = df.sample(min(len(df), 3000), random_state=42)
        schema = profile_schema(df)
        print(json.dumps(schema, indent=2, default=str))

        discrete_cols = df.select_dtypes(include=["object", "category", "bool"]).columns.tolist()
        generate_synthetic_data(input_path, output_path, df, user_inputs["num_rows"], discrete_cols)

    elif mode == "prompt":
        output_path = get_output_path(user_inputs["output_ext"], "textgen")
        fields = user_inputs.get("fields", [])
        if not fields:
            print("❌ No column names provided.")
            return

        few_shot = ",".join(fields) + "\n" + ",".join(["Example"] * len(fields))
        df = pd.DataFrame([x.split(",") for x in few_shot.split("\n")[1:]], columns=fields)
        schema = profile_schema(df)

        generate_text_data(schema, fields, user_inputs["use_case"], few_shot,
                           user_inputs["custom_prompt"], output_path, user_inputs["num_rows"])

    elif mode == "both":
        user_intent = input("Would you like to... Modify existing data then create synthetic data (ModGen), Create then enrich synthetic data (GenEn), or only modify current data (Mod)? Enter ModGen/GenEn/Mod: ").strip().lower()

        if user_intent not in ["modgen", "genen", "mod"]:
            print("❌ Invalid combo-mode selected.")
            return

        # ✅ Only collect input ONCE, now that we know the sub-mode
        user_inputs = collect_user_inputs("both")
        generate_combo_data(user_intent, user_inputs)

    else:
        print("❌ Invalid mode selected.")