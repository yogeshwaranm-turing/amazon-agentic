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
You are an expert JSON interpreter and AI instruction evaluator. I will give you a JSON object that contains: "instruction": A natural-language task given to an AI assistant "actions": A sequence of API calls made by the assistant, with arguments, outputs, and execution order "edges": Connections showing data flow between steps Your tasks are: 1. Summarize the JSON in plain English as a short story, explaining: - The original user's request/intention - The main steps the assistant took to fulfill it - The final outcome achieved 2. Analyze the instruction type based on these definitions: Procedural: Step-by-step feeding of instructions or “how to do something.” Goal-Oriented: Natural language, focuses on an outcome, avoids ambiguity, and lets the agent decide how to achieve it. 3. Final Verdict: Clearly state whether the overall set of actions is primarily Procedural or Goal-Oriented, and explain why in 2–3 sentences. 4. Check for the "No Assumption / No Hallucination" condition: Verify that every point in your summary and analysis is directly supported by the data in the JSON. Confirm with "No-Assumption Check": true only if no detail was added that is not in the JSON. 5. Check for Input Traceability in Actions: For each action in "actions", ensure that all of its input arguments are either: a) Explicitly given in the "instruction", or b) Are outputs from a previous function call (linked via "edges" or apparent from prior "actions" outputs). There must be no input values invented by the agent that are not traceable to user input or earlier action outputs. Confirm with "Input Traceability Check": true only if this is satisfied for all actions. Important Rules: Do not assume or infer anything that is not explicitly stated in the JSON. Base every detail strictly on the JSON content. No hallucinations — if a detail isn’t in the JSON or derived from prior outputs, do not mention it. Here is the JSON:
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
