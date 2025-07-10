import pandas as pd
import json
import os
from schema_profiler import load_dataframe, profile_schema
from combo_textgen import apply_prompt_to_data
from combo_ctgan import generate_from_dataframe
from utils import get_output_path, save_dataframe
from data_validator import validate
from privacy_postprocessing import interactive_privacy_postprocessing
from data_validator import THRESHOLDS
from utils import session_state
import uuid
from datetime import datetime
 
def generate_combo_data(mode: str, user_inputs: dict):
    session_state["generation_status"] = "saving inputs"
    print("🧠 user_inputs received:", user_inputs)

    try:
        input_path = user_inputs["input_path"]
        print("📁 Attempting to load:", input_path)
    except Exception as e:
        print("💥 Failed to get input_path from user_inputs:", e)
        session_state["generation_status"] = f"error: {str(e)}"
        return
    
    df = load_dataframe(input_path)
    df = df.sample(min(len(df), 3000), random_state=42)
    output_ext = user_inputs.get("output_ext", "csv")
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4().hex[:6]
    output_filename = f"synthetic_output_{timestamp}_{unique_id}.{output_ext}"
    output_path = os.path.join("outputs", output_filename)

    if mode.lower() == "modgen":
        print("✏️ Applying AI transformations using prompt...")
        session_state["generation_status"] = "executing prompt"
        try:
            transformed_df = apply_prompt_to_data(df, user_inputs["custom_prompt"])
        except Exception as e:
            print("❌ Failed during prompt transformation:")
            print(e)
            return
        session_state["generation_status"] = "prompt done, running ctgan"
        print("🤖 Generating synthetic data from transformed dataset...")
        try:
            synthetic_data = generate_from_dataframe(transformed_df, output_path, user_inputs["num_rows"])
        except Exception as e:
            print("❌ Failed during CTGAN generation:")
            print(e)
            return
        # prompts for privacy setting
        synthetic_data, privacy_report = interactive_privacy_postprocessing(synthetic_data)
        
        # Validate synthetic data
        results = validate(df, synthetic_data)
        avg_corr_diff = results["_pairwise_correlation"]["average_correlation_difference"]
        session_state["validation_results"] = results

        print("🔒 Privacy postprocessing report:")
        for k, v in privacy_report.items():
            print(f"  {k}: {v}")

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
        print(f"\n📈 OVERALL DATASET SIMILARITY SCORE : {1 - avg_corr_diff:.4f}")

        save_dataframe(synthetic_data, output_path)
        print(f"✅ Combined ModGen synthetic data saved to: {output_path}")

        # Store the path for downloading later
        session_state["output_path"] = output_path
        session_state["generation_status"] = "completed"

    elif mode.lower() == "genen":
        print("Generating base synthetic data from original dataset...")
        try:
            base_output_path = get_output_path(output_ext, "ctgan_base")
            synthetic_data=generate_from_dataframe(df, base_output_path, user_inputs["num_rows"])
        except Exception as e:
            print("❌ Failed during CTGAN generation:")
            print(e)
            return

        print("✏️ Re-loading and applying AI enrichment using prompt...")
        #base_df = load_dataframe(base_output_path)
        try:
            enriched_df = apply_prompt_to_data(synthetic_data, user_inputs["custom_prompt"])
        except Exception as e:
            print("❌ Failed during enrichment prompt:")
            print(e)
            return

        enriched_df, privacy_report = interactive_privacy_postprocessing(enriched_df)
        
        # Validate synthetic data
        results = validate(df, enriched_df)
        avg_corr_diff = results["_pairwise_correlation"]["average_correlation_difference"]
        session_state["validation_results"] = results

        print("🔒 Privacy postprocessing report:")
        for k, v in privacy_report.items():
            print(f"  {k}: {v}")

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
        print(f"\n📈 OVERALL DATASET SIMILARITY SCORE : {1 - avg_corr_diff:.4f}")

        save_dataframe(enriched_df, output_path)
        print(f"✅ Combined GenEn enriched data saved to: {output_path}")

        # Store the path for downloading later
        session_state["output_path"] = output_path
        session_state["generation_status"] = "completed"


    elif mode.lower() == "mod":
        print("✏️ Applying AI prompt to modify only original data...")
        try:
            mod_df = apply_prompt_to_data(df, user_inputs["custom_prompt"])
        except Exception as e:
            print("❌ Failed during AI modification:")
            print(e)
            return

        mod_df, privacy_report = interactive_privacy_postprocessing(mod_df)
        
        
        print("🔒 Privacy postprocessing report:")
        for k, v in privacy_report.items():
            print(f"  {k}: {v}")

    
        save_dataframe(mod_df, output_path)
        print(f"✅ Modified dataset saved to: {output_path}")

        # Store the path for downloading later
        session_state["output_path"] = output_path

    else:
        print("❌ Invalid combined mode provided. Must be one of: ModGen, GenEn, Mod")
    session_state["generation_status"] = "completed"
