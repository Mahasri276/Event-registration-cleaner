import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = """
You are an information extraction assistant for an Event Registration Cleaner.

Your job is ONLY to extract facts that are explicitly present in the registration entry.

Extract exactly these five fields:
- name
- phone
- email
- year
- branch

Rules:
1. Copy the information from the original entry.
2. Do NOT correct phone numbers.
3. Do NOT correct email addresses.
4. Do NOT invent missing information.
5. If a field is missing, return null.
6. Convert year words such as "1st year", "II year", "III yr",
   "IV year", and "final year" into numbers 1, 2, 3, or 4.
7. Return only valid JSON.
"""

def extract_registration(entry):
    prompt = SYSTEM_PROMPT + f"""

Registration entry:
{entry}

Return JSON in exactly this format:
{{
    "name": null,
    "phone": null,
    "email": null,
    "year": null,
    "branch": null
}}
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        return json.loads(text)

    except Exception as e:
        print("Gemini extraction failed:", e)
        return None


if __name__ == "__main__":

    test_entry = (
        "Name: Priya K, ph 98400 12345, "
        "email PRIYA.K@gmail.com, 2nd yr CSE"
    )

    result = extract_registration(test_entry)

    print("\nGemini Extraction Result:")
    print(json.dumps(result, indent=4))