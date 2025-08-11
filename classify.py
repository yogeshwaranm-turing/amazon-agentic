import json
import sys
import os
from openai import OpenAI

def classify_text(text):
    client = OpenAI(api_key=os.environ["OPEN_AI_KEY"])
    prompt = f"""
    You are given a text. Classify it as either:
    - Procedural: If it contains step-by-step instructions for doing something.
    - Outcome-Oriented: If it describes the result to be achieved without step-by-step details.

    Respond only with one word: "Procedural" or "Outcome".
    Text: {text}
    """
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )
    return response.output_text.strip()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python classify.py <json_file>")
        sys.exit(1)

    file_path = sys.argv[1]
    with open(file_path, "r") as f:
        data = json.load(f)

    text_to_check = data.get("task", "")
    if not text_to_check:
        print(f"No 'task' field found in {file_path}")
        sys.exit(1)

    classification = classify_text(text_to_check)
    print(f"Classification for {file_path}: {classification}")
