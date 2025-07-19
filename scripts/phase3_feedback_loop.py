import os
import google.generativeai as genai
from dotenv import load_dotenv
from phase2_translation_agent import translate_dialect # Still used for the initial translation

load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_API_KEY)
# Use a powerful model for the feedback loop to ensure high-quality data
feedback_model = genai.GenerativeModel('gemini-1.5-pro-latest')

def run_feedback_loop(text: str) -> str:
    """
    Runs the full feedback loop using only Gemini:
    1. Get initial translation from the base Gemini model.
    2. Use a Correction Agent (Gemini 1.5 Pro) to refine it.
    3. Use a Comparison Agent (Gemini 1.5 Pro) to validate the meaning.
    """
    print(f"--- Running Gemini Feedback Loop for: '{text}' ---")

    # 1. Initial Translation (from Phase 2)
    initial_translation = translate_dialect(text)
    print(f"  Initial Gemini Translation: '{initial_translation}'")

    # 2. Correction Agent (Gemini 1.5 Pro)
    correction_prompt = f"""
    The following phrase is a standard English translation of a Caribbean dialect.
    Review it for grammatical correctness, clarity, and natural phrasing.
    If it's good, return it as is. If not, provide a corrected, more accurate version.

    Original Dialect: "{text}"
    Initial Translation: "{initial_translation}"

    Corrected Translation:
    """
    
    try:
        correction_response = feedback_model.generate_content(correction_prompt)
        corrected_translation = correction_response.text.strip()
        print(f"  Correction Agent (Gemini 1.5 Pro): '{corrected_translation}'")
    except Exception as e:
        print(f"  Correction Agent failed: {e}")
        corrected_translation = initial_translation # Fallback

    # 3. Comparison Agent (Gemini 1.5 Pro)
    comparison_prompt = f"""
    Compare the original dialect phrase with the final translation.
    Does the translation accurately preserve the core meaning and nuance of the original?
    Answer with "Yes" or "No", followed by a brief explanation.

    Original Dialect: "{text}"
    Final Translation: "{corrected_translation}"

    Analysis:
    """

    try:
        comparison_response = feedback_model.generate_content(comparison_prompt)
        comparison_result = comparison_response.text.strip()
        print(f"  Comparison Agent (Gemini 1.5 Pro): {comparison_result}")

        if "no" in comparison_result.lower():
            print("  Warning: Translation may not fully match original meaning.")
            # In a real application, you might trigger a human review here.

    except Exception as e:
        print(f"  Comparison Agent failed: {e}")

    return corrected_translation

if __name__ == "__main__":
    # Test cases
    test_phrases = [
        "Mi soon come.",
        "She a real boss.",
        "De party did shot.",
    ]

    for phrase in test_phrases:
        final_translation = run_feedback_loop(phrase)
        print(f"  Final Validated Translation: '{final_translation}'\n")