import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_API_KEY)

# --- Configuration ---
# IMPORTANT: Replace this with the name of your fine-tuned model
# You can find this in the output of the fine-tuning job.
CUSTOM_MODEL_NAME = "tunedModels/dialect-translator-gemini-..." 

def run_custom_translation_pipeline(text: str) -> str:
    """
    Translates a dialect phrase using the fine-tuned Gemini model.
    """
    if "..." in CUSTOM_MODEL_NAME:
        return "Error: Please update CUSTOM_MODEL_NAME with your fine-tuned model's name."

    model = genai.GenerativeModel(CUSTOM_MODEL_NAME)
    
    print(f"--- Running Custom Translation for: '{text}' ---")
    
    try:
        # The prompt format should match what the model was trained on
        prompt = f"Translate the following Caribbean dialect phrase to standard English: \"{text}\""
        response = model.generate_content(prompt)
        translation = response.text.strip()
        print(f"  Fine-tuned Gemini Translation: '{translation}'")
        return translation
    except Exception as e:
        print(f"Error using fine-tuned Gemini model: {e}")
        return f"Error: Could not translate '{text}' with custom model."

if __name__ == "__main__":
    test_phrases = [
        "Mi soon come.",
        "She a real boss.",
        "De party did shot.",
    ]

    for phrase in test_phrases:
        translation = run_custom_translation_pipeline(phrase)
        print(f"  Final Result: '{translation}'\n")