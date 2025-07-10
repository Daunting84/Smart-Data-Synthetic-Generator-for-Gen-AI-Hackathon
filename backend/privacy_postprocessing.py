import numpy as np
import pandas as pd
from utils import selected_values

def add_gaussian_noise(df, noise_std=0.1, columns=None):
    """Add Gaussian noise to numerical columns."""
    df = df.copy()
    if columns is None:
        columns = df.select_dtypes(include=[np.number]).columns
    for col in columns:
        noise = np.random.normal(0, noise_std, size=len(df))
        df[col] = df[col] + noise
    return df

def category_swap(df, swap_fraction=0.1, columns=None):
    """Randomly swap categories in categorical columns."""
    df = df.copy()
    if columns is None:
        columns = df.select_dtypes(include=['object', 'category']).columns
    for col in columns:
        n_swap = int(len(df) * swap_fraction)
        swap_indices = np.random.choice(df.index, size=n_swap, replace=False)
        shuffled_values = df.loc[swap_indices, col].sample(frac=1).values
        df.loc[swap_indices, col] = shuffled_values
    return df

def mask_data(df, mask_columns=None, mask_value="***MASKED***"):
    """Mask specified columns with a fixed mask value."""
    df = df.copy()
    if mask_columns is None:
        return df  # nothing to mask
    for col in mask_columns:
        if col in df.columns:
            df[col] = mask_value
    return df

def privacy_report(noise_std, swap_fraction, masked_columns):
    report = {
        "Gaussian noise std dev": noise_std,
        "Category swap fraction": swap_fraction,
        "Masked columns": masked_columns or []
    }
    return report

def interactive_privacy_postprocessing(synthetic_data):
    privacy = selected_values.get("privacy", {})
    noise_std = float(privacy.get("noise_stddev", 0))
    swap_fraction = float(privacy.get("category_swap_fraction", 0))
    mask_columns = privacy.get("masked_columns", [])

    if noise_std > 0:
        synthetic_data = add_gaussian_noise(synthetic_data, noise_std=noise_std)
        print(f"Applied Gaussian noise with stddev {noise_std}")

    if swap_fraction > 0:
        synthetic_data = category_swap(synthetic_data, swap_fraction=swap_fraction)
        print(f"Applied category swapping with fraction {swap_fraction}")

    if mask_columns:
        synthetic_data = mask_data(synthetic_data, mask_columns=mask_columns)
        print(f"Masked columns: {', '.join(mask_columns)}")

    report = {
        "noise_stddev": noise_std,
        "category_swap_fraction": swap_fraction,
        "masked_columns": mask_columns
    }
    return synthetic_data, report
