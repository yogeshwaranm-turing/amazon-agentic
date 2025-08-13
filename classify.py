import json
import sys
import os
import anthropic

# Get the file path from arguments
file_path = sys.argv[1]

# Read API key from environment variable
api_key = os.getenv("ANTHROPIC_API_KEY")
if not api_key:
    raise EnvironmentError("❌ Error: ANTHROPIC_API_KEY not found in environment variables.")

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=api_key)

# Load the full JSON file
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Convert JSON to a formatted string
json_str = json.dumps(data, indent=2)

# Prompt for classification
prompt = f"""
Classify the following JSON instructions as either:
1. Procedural (step-by-step instructions), or
2. Outcome-oriented (goal/result focused).

Return only the classification.

JSON content:
{json_str}
"""

# Call Claude 3.5 Sonnet
response = client.messages.create(
    model="claude-3-5-sonnet-20240620",  # latest Claude 3.5 Sonnet
    max_tokens=8000,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

# Output the result
print("Classification result:", response.content[0].text.strip())
