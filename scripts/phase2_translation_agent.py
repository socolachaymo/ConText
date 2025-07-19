import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def translate_dialect(text: str) -> str:
    """
    Translates a dialectal phrase to standard English using a few-shot prompt.
    """
    prompt = f"""
    Translate the following Caribbean dialect phrase to standard English.
    Your goal is to preserve the original meaning, including idioms and cultural nuances.

    **Examples:**
    - Dialect: "Mi soon come."
      Standard English: "I will be right back."
    - Dialect: "Wagwan?"
      Standard English: "What's going on?" or "How are you?"
    - Dialect: "De ting sell off."
      Standard English: "The event was very successful and sold out."
    - Dialect: "She a real topanaris."
      Standard English: "She is a highly respected and important person."

    **Translate this phrase:**
    - Dialect: "{text}"
      Standard English:
    """

    try:
        response = model.generate_content(prompt)
        translation = response.text.strip()
        return translation
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return f"Error: Could not translate '{text}'"

if __name__ == "__main__":
    # Test cases
    test_phrases = [
        "Mi deh yah.",
        "Everyting criss.",
        "De food did sweet.",
        "Him a idiat.",
    ]

    print("--- Dialect Translation Test ---")
    for phrase in test_phrases:
        translation = translate_dialect(phrase)
        print(f"Dialect: '{phrase}'")
        print(f"Translation: '{translation}'\n")