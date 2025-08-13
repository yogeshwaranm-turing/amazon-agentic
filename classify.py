import json
import sys
import openai
import os

file_path = sys.argv[1]
openai.api_key = os.environ["OPEN_AI_KEY"]

# Load the full JSON
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Convert JSON to a nicely formatted string
json_str = json.dumps(data, indent=2)

prompt = f"""
Classify the following JSON instructions as either:
1. Procedural (step-by-step instructions), or
2. Outcome-oriented (goal/result focused).

JSON content:
{json_str}
"""

response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}],
    temperature=0
)

print("Classification result:", response.choices[0].message["content"].strip())
