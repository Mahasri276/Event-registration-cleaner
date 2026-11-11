import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


def test_gemini():
    if not API_KEY:
        print("ERROR: Gemini API key not found in .env")
        return

    try:
        client = genai.Client(api_key=API_KEY)

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents="Say: Gemini connection successful!"
        )

        print("Gemini connection successful!")
        print(response.text)

    except Exception as e:
        print("Gemini connection failed!")
        print("Error:", e)


if __name__ == "__main__":
    test_gemini()