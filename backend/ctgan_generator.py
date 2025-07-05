from ctgan import CTGAN
from joblib import parallel_backend
import pandas as pd
import os
import json
from data_validator import validate
from data_validator import THRESHOLDS
from privacy_postprocessing import interactive_privacy_postprocessing


def generate_synthetic_data(input_path, output_path, df, num_rows=1000, discrete_columns=None):
    print("🔧 Training CTGAN model...")
    model = CTGAN(epochs=100)

    # Ensure training is stable
    with parallel_backend("loky", n_jobs=1):
        model.fit(df, discrete_columns=discrete_columns)

    print("✅ Model training complete. Generating synthetic data...")
    synthetic_data = model.sample(num_rows)

    # prompts for privacy setting
    synthetic_data, privacy_report = interactive_privacy_postprocessing(synthetic_data)
    print("🔒 Privacy postprocessing report:")
    for k, v in privacy_report.items():
        print(f"  {k}: {v}")

     # Validate synthetic data
    results = validate(df, synthetic_data)

    print("📊 Validation Results:")
    for feature, stats in results.items():
        if feature == "_pairwise_correlation":
            print("\n🧩 Pairwise Correlation Analysis:")
            avg_corr_diff = stats['average_correlation_difference']
            flag = " ⚠️" if avg_corr_diff > THRESHOLDS["average_correlation_difference"] else ""
            print(f"  🔢 Avg Correlation Difference: {avg_corr_diff:.4f}{flag}")

            print("  🧪 Per-feature differences:")
            for col1, subdict in stats["per_feature_difference"].items():
                for col2, val in subdict.items():
                    print(f"    {col1} vs {col2}: {val:.4f}")
        else:
            print(f"\n🔍 {feature}:")
            for metric, value in stats.items():
                if isinstance(value, (int, float)):
                    flag = " ⚠️" if metric in THRESHOLDS and value > THRESHOLDS[metric] else ""
                    print(f"  {metric}: {value:.4f}{flag}")
                else:
                    print(f"  {metric}: {value}")

    print("\n⚠️ = Flagged values may indicate lower similarity or data quality issues.")
    avg_corr_diff = results["_pairwise_correlation"]["average_correlation_difference"]
    print(f"\n📈 OVERALL DATASET SIMILARITY SCORE : {1 - avg_corr_diff:.4f}")

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
