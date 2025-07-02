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
    user_inputs = collect_user_inputs(mode)
    decide_model(mode, user_inputs)

if __name__ == "__main__":
    main()