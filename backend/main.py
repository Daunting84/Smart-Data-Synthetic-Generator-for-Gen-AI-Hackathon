### main.py

import os
import time
import joblib
import pandas as pd
import json
from dotenv import load_dotenv

from schema_profiler import load_dataframe, profile_schema
from model_dispatcher import decide_model
from utils import get_output_path, collect_user_inputs

# Ensure parallel processing doesn't crash
os.environ["JOBLIB_MULTIPROCESSING"] = "0"
joblib.parallel.DEFAULT_N_JOBS = 1

# Load .env variables
load_dotenv()

def main():
    mode = input("What do you want to provide? (data/prompt/both): ").strip().lower()
    if mode not in ["data", "prompt", "both"]:
        print("❌ Invalid mode selected.")
        exit(1)
    user_intent = None
    if mode=="both":
        user_intent = input("Would you like to... Modify existing data then create synthetic data (ModGen), Create then enrich synthetic data (GenEn), or only modify current data (Mod)? Enter ModGen/GenEn/Mod: ").strip().lower()
        if user_intent not in ["modgen", "genen", "mod"]:
            print("❌ Invalid combo-mode selected.")
            exit(1)
    user_inputs = collect_user_inputs(mode,user_intent=user_intent)
    decide_model(mode, user_inputs,user_intent=user_intent)

if __name__ == "__main__":
    main()