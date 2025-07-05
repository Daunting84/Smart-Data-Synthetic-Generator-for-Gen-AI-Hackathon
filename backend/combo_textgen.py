import os
import json
import requests
import pandas as pd
from io import StringIO
from dotenv import load_dotenv

load_dotenv()

def call_openrouter_combo(prompt, model="mistralai/mistral-7b-instruct", temperature=0.7):
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("❌ OPENROUTER_API_KEY not found in environment variables.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "HTTP-Referer": "https://your-domain.com",  # Update if deploying
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a synthetic data transformation assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"OpenRouter API Error: {response.status_code} - {response.text}")

def apply_prompt_to_data(df, prompt): 
    csv_data = df.to_csv(index=False)
    full_prompt = f"""
You are a synthetic data assistant. Modify the following CSV data based on the user's instructions.

User instructions:
{prompt}

CSV input:
{csv_data}

Return only the modified CSV output, no commentary.
"""
    response = call_openrouter_combo(full_prompt)
    try:
        df_modified = pd.read_csv(StringIO(response))
        return df_modified
    except Exception as e:
        print("❌ Failed to parse AI-transformed CSV.")
        print("Raw response:\n", response)
        raise e