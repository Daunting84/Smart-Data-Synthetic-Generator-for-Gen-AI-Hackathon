from ctgan import CTGAN
from joblib import parallel_backend
import pandas as pd
import os

def generate_from_dataframe(df, output_path, num_rows=1000):
    """
    Train a CTGAN model on the given dataframe and generate synthetic data.
    Saves the synthetic data to output_path.
    """
    print("🔧 Training CTGAN model on modified data...")
    model = CTGAN(epochs=100)

    with parallel_backend("loky", n_jobs=1):
        discrete_cols = df.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
        model.fit(df, discrete_columns=discrete_cols)

    synthetic_data = model.sample(num_rows)
    save_dataframe(synthetic_data, output_path)
    print(f"✅ Synthetic data saved to: {output_path}")

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