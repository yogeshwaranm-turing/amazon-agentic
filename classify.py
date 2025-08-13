import json
import sys
import os
from openai import OpenAI

# Get arguments
if len(sys.argv) < 2:
    print("❌ Error: No JSON file path provided.")
    sys.exit(1)

file_path = sys.argv[1]
print(f"📄 Reading JSON file: {file_path}")

# Get API key from env
api_key = os.getenv("OPEN_AI_KEY")
if not api_key:
    print("❌ Error: OPEN_AI_KEY not found in environment variables.")
    sys.exit(1)

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Load JSON file
try:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print(f"❌ Error: Invalid JSON format in {file_path}")
    print(f"Details: {e}")
    sys.exit(1)

# Convert JSON to a nicely formatted string
json_str = json.dumps(data, indent=2)

# Prompt for classification
prompt = f"""
Classify the following JSON instructions as either:
1. Procedural (step-by-step instructions), or
2. Outcome-oriented (goal/result focused).

JSON content:
{json_str}
"""

# Send request to LLM
try:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
except Exception as e:
    print(f"❌ Error calling OpenAI API: {e}")
    sys.exit(1)

# Output result
classification = response.choices[0].message["content"].strip()
print("✅ Classification result:", classification)
