from ctgan import CTGAN
from joblib import parallel_backend
import pandas as pd
import os
import json

def generate_synthetic_data(input_path, output_path, df, num_rows=1000, discrete_columns=None):
    print("🔧 Training CTGAN model...")
    model = CTGAN(epochs=100)

    # Ensure training is stable
    with parallel_backend("loky", n_jobs=1):
        model.fit(df, discrete_columns=discrete_columns)

    print("✅ Model training complete. Generating synthetic data...")
    synthetic_data = model.sample(num_rows)

    save_dataframe(synthetic_data, output_path)
    print(f"✅ Synthetic data saved to: {output_path}")


def save_dataframe(df, path):
    ext = os.path.splitext(path)[1].lower()

    # Default to .csv if no valid extension provided
    if ext not in [".csv", ".json", ".xls", ".xlsx"]:
        print("⚠️ Invalid or missing extension. Defaulting to .csv")
        path += ".csv"
        ext = ".csv"

    # Create output folder if needed
    output_dir = os.path.dirname(path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    if ext == '.csv':
        df.to_csv(path, index=False)
    elif ext == '.json':
        df.to_json(path, orient='records', indent=2)
    elif ext in ['.xls', '.xlsx']:
        df.to_excel(path, index=False)
    else:
        raise ValueError(f"❌ Unsupported output file format: {ext}")
