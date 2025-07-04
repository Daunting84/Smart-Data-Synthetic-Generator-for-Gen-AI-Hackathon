from ctgan import CTGAN
from joblib import parallel_backend
import pandas as pd
import os
from data_validator import validate

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
     # Validate synthetic data
    results = validate(df, synthetic_data)

    print("📊 Validation Results:")
    for feature, stats in results.items():
        if feature == "_pairwise_correlation":
            print("\n🧩 Pairwise Correlation Analysis:")
            print(f"  🔢 Avg Correlation Difference: {stats['average_correlation_difference']:.4f}")

            print("  🧪 Per-feature differences:")
            for col1, subdict in stats["per_feature_difference"].items():
                for col2, val in subdict.items():
                    print(f"    {col1} vs {col2}: {val:.4f}")
        else:
            print(f"\n🔍 {feature}:")
            for metric, value in stats.items():
                if isinstance(value, (int, float)):
                    print(f"  {metric}: {value:.4f}")
                else:
                    print(f"  {metric}: {value}")

    avg_corr_diff = results["_pairwise_correlation"]["average_correlation_difference"]
    print(f"\n📈 OVERALL DATASET SIMILARITY SCORE : {1 - avg_corr_diff:.4f}")

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