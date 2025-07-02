import pandas as pd
import json
from schema_profiler import load_dataframe, profile_schema
from combo_textgen import apply_prompt_to_data
from combo_ctgan import generate_from_dataframe
from utils import get_output_path

def run_combo_pipeline(mode: str, user_inputs: dict):
    input_path = user_inputs["input_path"]
    df = load_dataframe(input_path)
    df = df.sample(min(len(df), 3000), random_state=42)

    output_ext = user_inputs["output_ext"]
    output_path = get_output_path(output_ext, f"combo_{mode.lower()}")

    if mode.lower() == "modgen":
        print("✏️ Applying AI transformations using prompt...")
        try:
            transformed_df = apply_prompt_to_data(df, user_inputs["custom_prompt"])
        except Exception as e:
            print("❌ Failed during prompt transformation:")
            print(e)
            return

        print("🤖 Generating synthetic data from transformed dataset...")
        try:
            generate_from_dataframe(transformed_df, output_path, user_inputs["num_rows"])
        except Exception as e:
            print("❌ Failed during CTGAN generation:")
            print(e)
            return

        print(f"✅ Combined ModGen synthetic data saved to: {output_path}")

    elif mode.lower() == "genen":
        print("🤖 Generating base synthetic data from original dataset...")
        try:
            base_output_path = get_output_path(output_ext, "ctgan_base")
            generate_from_dataframe(df, base_output_path, user_inputs["num_rows"])
        except Exception as e:
            print("❌ Failed during CTGAN generation:")
            print(e)
            return

        print("✏️ Re-loading and applying AI enrichment using prompt...")
        base_df = load_dataframe(base_output_path)
        try:
            enriched_df = apply_prompt_to_data(base_df, user_inputs["custom_prompt"])
        except Exception as e:
            print("❌ Failed during enrichment prompt:")
            print(e)
            return

        enriched_output_path = get_output_path(output_ext, "genen_enriched")
        enriched_df.to_csv(enriched_output_path, index=False)
        print(f"✅ Combined GenEn enriched data saved to: {enriched_output_path}")

    elif mode.lower() == "mod":
        print("✏️ Applying AI prompt to modify only original data...")
        try:
            mod_df = apply_prompt_to_data(df, user_inputs["custom_prompt"])
        except Exception as e:
            print("❌ Failed during AI modification:")
            print(e)
            return

        mod_df.to_csv(output_path, index=False)
        print(f"✅ Modified dataset saved to: {output_path}")

    else:
        print("❌ Invalid combined mode provided. Must be one of: ModGen, GenEn, Mod")
