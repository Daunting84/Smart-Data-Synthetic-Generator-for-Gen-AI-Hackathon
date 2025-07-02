import pandas as pd
import os
import numpy as np
import json
from dateutil.parser import parse
import math
from collections import Counter

#determine file type
def load_dataframe(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.csv':
        return pd.read_csv(path)
    elif ext == '.json':
        return pd.read_json(path)
    elif ext in ['.xls', '.xlsx']:
        return pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

#delects if the column type is dates
def is_date(string, fuzzy=False):
    try:
        parse(string, fuzzy=fuzzy)
        return True
    except Exception:
        return False   
     
#detect data type of a panda series.(returns one of boolean, integer, float, datetime, categorical, text or mixed)
def detect_column_type(series:pd.Series,sample_size=1000):
    # Drop missing values for type inference
    non_null_series = series.dropna()

    # Sample for efficiency if very large
    if len(non_null_series) > sample_size:
        non_null_series = non_null_series.sample(sample_size, random_state=42)

    unique_vals = non_null_series.unique()
    unique_count = len(unique_vals)
    total_count = len(non_null_series)

    # If empty or all null
    if total_count == 0:
        return "unknown"

     # Check boolean: only two unique values and those values look boolean-ish
    bool_sets = [
        {True, False},
        {"true", "false"},
        {"True", "False"},
        {"yes", "no"},
        {"Yes", "No"},
        {1, 0},
        {"1", "0"},
    ]
    unique_vals_set = set(map(str, unique_vals))
    for bset in bool_sets:
        if unique_vals_set.issubset(set(map(str, bset))):
            return "boolean"
        
    #check if numeric    
    is_numeric=pd.api.types.is_numeric_dtype(non_null_series)
    if is_numeric:
        # Check if all floats are actually integers
        # Use tolerance for floating point precision
        floats_are_ints = non_null_series.apply(lambda x: math.isclose(x, round(x), abs_tol=1e-9)).all()
        if floats_are_ints:
            return "integer"
        else:
            return "float"
        
    # Check datetime by trying to parse some samples
    # Use a subset of unique values for speed
    date_checks = non_null_series.astype(str).apply(is_date)
    if date_checks.mean() > 0.8:  # 80%+ parseable as date
        return "datetime"

    # Distinguish categorical vs text by heuristics:
    # cardinality ratio (unique/total), avg length, entropy, presence of spaces
    cardinality_ratio = unique_count / total_count
    avg_len = non_null_series.astype(str).apply(len).mean()
    
    # Entropy of the values
    counts = Counter(non_null_series)
    probs = [count / total_count for count in counts.values()]
    entropy = -sum(p * np.log2(p) for p in probs if p > 0)

    # Presence of whitespace in values
    whitespace_ratio = non_null_series.astype(str).apply(lambda x: ' ' in x).mean()

    # Rules for categorical vs text
    if cardinality_ratio < 0.05 and avg_len < 20 and entropy < 4 and whitespace_ratio < 0.2:
        return "categorical"
    else:
        return "text"


#Creates a profile of each data column
def profile_schema(df: pd.DataFrame):
    """
    Profile a dataframe and return a dictionary with column type and summary statistics.
    """
    schema = {}

    for col in df.columns:
        col_data = df[col]
        col_type = detect_column_type(col_data)

        col_summary = {
            "type": col_type,
            "num_missing": col_data.isna().sum(),
            "num_unique": col_data.nunique(),
        }

        if col_type in ["integer", "float"]:
            col_summary.update({
                "mean": col_data.mean(),
                "std": col_data.std(),
                "min": col_data.min(),
                "max": col_data.max(),
            })

        if col_type == "categorical":
            top_vals = col_data.value_counts().head(5).to_dict()
            col_summary.update({
                "top_values": top_vals,
            })

        if col_type == "boolean":
            counts = col_data.value_counts(dropna=False).to_dict()
            col_summary.update({
                "counts": counts,
            })

        if col_type == "datetime":
            col_summary.update({
                "min_date": col_data.min(),
                "max_date": col_data.max(),
            })

        # Add more if needed for text, mixed, etc.

        schema[col] = col_summary

    return schema