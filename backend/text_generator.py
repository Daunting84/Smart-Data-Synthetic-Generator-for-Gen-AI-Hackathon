import os
import requests
import pandas as pd
import json
from io import StringIO
from textwrap import dedent
from utils import session_state

def build_field_aware_prompt(schema: dict, use_case: str, num_rows: int, custom_prompt: str, few_shot_examples: str, format_name) -> str:
    field_descriptions = []
    for col, info in schema.items():
        col_type = info["type"]
        if col_type == "datetime":
            field_descriptions.append(f"{col} (date)")
        elif col_type == "boolean":
            field_descriptions.append(f"{col} (true/false)")
        elif col_type == "categorical":
            top_vals = info.get("top_values", {})
            example_vals = ', '.join(list(top_vals.keys())[:3])
            field_descriptions.append(f"{col} (category, e.g., {example_vals})")
        elif col_type == "integer":
            field_descriptions.append(f"{col} (integer)")
        elif col_type == "float":
            field_descriptions.append(f"{col} (decimal number)")
        else:
            field_descriptions.append(f"{col}")

    formatted_fields = ', '.join(field_descriptions)

    prompt = f"""
Generate {num_rows} realistic examples of {use_case} in {format_name} format.

Fields and types:
{formatted_fields}

Examples:
{few_shot_examples}

Additional instructions:
{custom_prompt}

RULES:
Use consistent formatting, no extra blank lines.
Use reasonable numeric ranges for the given catagory
Output dates in YYYY-MM-DD format
Avoid commas inside fields or properly escape them.
If a field contains commas, wrap it in double quotes. For example:
name,message
Steve,"Hello, world"

Please output only {format_name} content with headers, no explanations or extra text.
Generate diverse and realistic examples, not repeating the same data.
If you cannot generate valid {format_name}, respond with an error message only.
"""
    return prompt.strip()

def call_openrouter(prompt, model="mistralai/mistral-7b-instruct", temperature=0.7):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("❌ OPENROUTER_API_KEY not found in environment variables.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://your-domain.com",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a synthetic text data generator."},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"OpenRouter API Error: {response.status_code} - {response.text}")

def save_dataframe(df, path):
    ext = os.path.splitext(path)[1].lower()
    if ext == '.csv':
        df.to_csv(path, index=False)
    elif ext == '.json':
        df.to_json(path, orient='records', indent=2)
    elif ext in ['.xls', '.xlsx']:
        df.to_excel(path, index=False)
    else:
        raise ValueError(f"Unsupported output file format: {ext}")

def generate_text_data(schema, fields, use_case, few_shot_examples, custom_prompt, output_path, num_rows=10):
    ext = os.path.splitext(output_path)[1].lower().strip(".")
    format_name = ext.upper()

    prompt = build_field_aware_prompt(schema, use_case, num_rows, custom_prompt, few_shot_examples, format_name)

    print("🟡 Sending prompt to OpenRouter...")
    response_text = call_openrouter(prompt)

    try:
        if ext == "csv":
            df = pd.read_csv(StringIO(response_text))
        elif ext == "json":
            data = json.loads(response_text)
            df = pd.json_normalize(data)
        elif ext in ["xls", "xlsx"]:
            df = pd.read_csv(StringIO(response_text))
        else:
            raise ValueError(f"❌ Unsupported output file format: {ext}")

        save_dataframe(df, output_path)
        print(f"✅ Synthetic text data saved to: {output_path}")
        session_state["output_path"] = output_path

    except Exception as e:
        print("❌ Failed to parse response into DataFrame.")
        print("Raw response:\n", response_text)
        raise e
    session_state["generation_status"] = "completed"
