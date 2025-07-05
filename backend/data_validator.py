import pandas as pd
import numpy as np
from scipy.stats import ks_2samp, chi2_contingency, wasserstein_distance
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns


def ks_test(real_col, synth_col):
    statistic, p_value = ks_2samp(real_col, synth_col)
    return {"ks_stat": statistic, "p_value": p_value}


def wasserstein(real_col, synth_col):
    distance = wasserstein_distance(real_col, synth_col)
    return {"wasserstein_distance": distance}


def chi_square(real_col, synth_col):
    real_freq = real_col.value_counts()
    synth_freq = synth_col.value_counts()

    all_categories = sorted(set(real_freq.index).union(set(synth_freq.index)))
    real_counts = [real_freq.get(cat, 0) for cat in all_categories]
    synth_counts = [synth_freq.get(cat, 0) for cat in all_categories]

    try:
        chi2, p, _, _ = chi2_contingency([real_counts, synth_counts])
        return {"chi2_stat": chi2, "p_value": p}
    except ValueError:
        return {"chi2_stat": None, "p_value": None, "error": "Insufficient category count."}


def total_variation_distance(real_col, synth_col):
    real_freq = real_col.value_counts(normalize=True)
    synth_freq = synth_col.value_counts(normalize=True)

    all_categories = sorted(set(real_freq.index).union(set(synth_freq.index)))
    tvd = 0.5 * sum(abs(real_freq.get(cat, 0) - synth_freq.get(cat, 0)) for cat in all_categories)
    return {"tvd": tvd}

def compare_correlations(real_df, synth_df):
    real_corr = real_df.corr(numeric_only=True)
    synth_corr = synth_df.corr(numeric_only=True)

    diff = (real_corr - synth_corr).abs()
    avg_diff = diff.mean().mean()

    return {
        "average_correlation_difference": avg_diff,
        "per_feature_difference": diff.to_dict()
    }

def plot_correlation_heatmaps(real_df, synth_df):
    import matplotlib.pyplot as plt
    import seaborn as sns

    real_corr = real_df.corr(numeric_only=True)
    synth_corr = synth_df.corr(numeric_only=True)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    sns.heatmap(real_corr, ax=axes[0], cmap="coolwarm", annot=True)
    axes[0].set_title("Real Data Correlation Matrix")

    sns.heatmap(synth_corr, ax=axes[1], cmap="coolwarm", annot=True)
    axes[1].set_title("Synthetic Data Correlation Matrix")

    plt.tight_layout()
    plt.show()

def determine_column_type(series):
    if pd.api.types.is_numeric_dtype(series):
        return "numerical"
    elif pd.api.types.is_datetime64_any_dtype(series):
        return "datetime"
    else:
        return "categorical"

THRESHOLDS = {
    "ks_stat": 0.3,              # > 0.3 may indicate mismatch
    "wasserstein_distance": 10, # domain-dependent, adjust as needed
    "chi2_stat": 10,            # high chi2 may signal distribution drift
    "tvd": 0.2,                 # total variation > 0.2 is moderate mismatch
    "average_correlation_difference": 0.15  # overall difference
}


def validate(real_df: pd.DataFrame, synth_df: pd.DataFrame) -> dict:
    results = defaultdict(dict)
    common_columns = set(real_df.columns).intersection(set(synth_df.columns))

    for col in common_columns:
        real_col = real_df[col].dropna()
        synth_col = synth_df[col].dropna()

        col_type = determine_column_type(real_col)
        if col_type == "numerical":
            results[col]["type"] = "numerical"
            results[col].update(ks_test(real_col, synth_col))
            results[col].update(wasserstein(real_col, synth_col))

        elif col_type == "categorical":
            results[col]["type"] = "categorical"
            results[col].update(chi_square(real_col, synth_col))
            results[col].update(total_variation_distance(real_col, synth_col))

        elif col_type == "datetime":
            # Convert datetimes to timestamps for Wasserstein + KS
            real_ts = real_col.astype(np.int64) // 10**9
            synth_ts = synth_col.astype(np.int64) // 10**9
            results[col]["type"] = "datetime"
            results[col].update(ks_test(real_ts, synth_ts))
            results[col].update(wasserstein(real_ts, synth_ts))
    # Add pairwise correlation analysis
    correlation_summary = compare_correlations(real_df, synth_df)
    results["_pairwise_correlation"] = correlation_summary
    #print(f"📊 Avg Correlation Diff: {results['_pairwise_correlation']['average_correlation_difference']:.4f}")

    return dict(results)
