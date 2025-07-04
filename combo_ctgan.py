from ctgan import CTGAN
from joblib import parallel_backend
import pandas as pd
import os

from data_validator import THRESHOLDS


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

    
    return synthetic_data