import json
import sys
import os
import anthropic
import re
import sys


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
You are an expert JSON interpreter and AI instruction evaluator.

I will give you a JSON object that contains:
- "instruction": A natural-language task given to an AI assistant
- "actions": A sequence of API calls made by the assistant, with arguments, outputs, and execution order
- "edges": Connections showing data flow between steps

Your tasks are:

1. Summarize the JSON in plain English as a short story, explaining:
   - The original user's request/intention
   - The main steps the assistant took to fulfill it
   - The final outcome achieved

2. Analyze the instruction type based on these definitions:
   - Procedural: Step-by-step feeding of instructions or “how to do something.”
   - Goal-Oriented: Natural language, focuses on an outcome, avoids ambiguity, and lets the agent decide how to achieve it.

3. Final Verdict: Clearly state whether the overall set of actions is primarily Procedural or Goal-Oriented, and explain why in 2–3 sentences.

4. Check for the "No Assumption / No Hallucination" condition:
   Verify that every point in your summary and analysis is directly supported by the data in the JSON.
   Confirm with "No-Assumption Check": true only if no detail was added that is not in the JSON.

5. Check for Input Traceability in Actions:
   For each action in "actions", ensure that all of its input arguments are either:
     a) Explicitly given in the "instruction", or
     b) Are outputs from a previous function call (linked via "edges" or apparent from prior "actions" outputs).
   There must be no input values invented by the agent that are not traceable to user input or earlier action outputs.
   Confirm with "Input Traceability Check": true only if this is satisfied for all actions.

---

✅ Additional Pass/Fail Criteria:

1. **User-facing** — User Facing means the user is not in control and dosent have direct access but the agent does

2. **Goal/Output-oriented** — The instruction must be outcome-focused.  
   If it is process-oriented or step-by-step procedural, fail.

3. **Unambiguous input** —  — The provided instruction must be precise and explicit. 
    All details should be clearly stated without vague terms. 
    For example, instead of saying “evening,” it should specify “3:00 PM.” 
    If any part of the instruction leaves room for interpretation, fail.

---

Return your analysis in **two parts**:

**Part 1 — Full Analysis** (same as before):
- Summary
- Instruction Type Analysis
- Final Verdict
- No-Assumption Check
- Input Traceability Check

**Part 2 — Criteria Check** (exact format below):

User-Facing: Yes/No  
Goal-Oriented: Yes/No  
Ambiguous input : Yes/No  
Reasoning: <short reasoning for each check>  
Verdict: Pass/Fail  

Here is the JSON:
{json_str}
"""

# Call Claude 3.5 Sonnet
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=8000,
    messages=[
        {"role": "user", "content": prompt}
    ]
)

output_text = response.content[0].text.strip()

# Output the result
print("Classification Raw Output:\n", output_text)

# --- Part 2 parsing ---
cleaned_text = re.sub(r"\*+", "", output_text)

user_facing = re.search(r"User-Facing:\s*(Yes|No)", cleaned_text, re.IGNORECASE)
goal_oriented = re.search(r"Goal-Oriented:\s*(Yes|No)", cleaned_text, re.IGNORECASE)
ambiguous_input = re.search(r"Ambiguous input:\s*(Yes|No)", cleaned_text, re.IGNORECASE)
verdict = re.search(r"Verdict:\s*(Pass|Fail)", cleaned_text, re.IGNORECASE)

fail_reason = []

if not user_facing or user_facing.group(1).lower() != "yes":
    fail_reason.append("❌ Not user-facing.")

if not goal_oriented or goal_oriented.group(1).lower() != "yes":
    fail_reason.append("❌ Not goal-oriented.")

if not ambiguous_input or ambiguous_input.group(1).lower() != "no":
    fail_reason.append("❌ Ambiguous input.")

if verdict and verdict.group(1).lower() == "fail":
    fail_reason.append("❌ Claude marked as fail.")

if fail_reason:
    with open("result.txt", "w", encoding="utf-8") as f:
        f.write(output_text + "\n")
        f.write("\n".join(fail_reason) + "\n")
else:
    with open("result.txt", "w", encoding="utf-8") as f:
        f.write(output_text + "\n")
        f.write("✅ All checks passed.\n")
