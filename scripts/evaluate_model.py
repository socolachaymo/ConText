import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=GEMINI_API_KEY)

# --- Configuration ---
# IMPORTANT: Replace this with the name of your fine-tuned model
CUSTOM_MODEL_NAME = "tunedModels/dialect-translator-gemini-..."

def evaluate_model(validation_file="data/validation.jsonl"):
    """
    Evaluates the fine-tuned Gemini model against the validation set and calculates the BLEU score.
    """
    if "..." in CUSTOM_MODEL_NAME:
        print("Error: Please update CUSTOM_MODEL_NAME with your fine-tuned model's name.")
        return

    if not os.path.exists(validation_file):
        print(f"Error: Validation file not found at {validation_file}")
        return

    model = genai.GenerativeModel(CUSTOM_MODEL_NAME)
    
    with open(validation_file, "r") as f:
        validation_data = [json.loads(line) for line in f]

    total_bleu_score = 0
    chencherry = SmoothingFunction()

    print(f"--- Evaluating model '{CUSTOM_MODEL_NAME}' on {len(validation_data)} samples ---")

    for i, item in enumerate(validation_data):
        prompt = item['input_text']
        reference_translation = item['output_text']

        try:
            # Get the model's translation
            response = model.generate_content(prompt)
            model_translation = response.text.strip()

            # Calculate BLEU score
            reference = [reference_translation.split()]
            candidate = model_translation.split()
            bleu_score = sentence_bleu(reference, candidate, smoothing_function=chencherry.method1)
            total_bleu_score += bleu_score

            print(f"\nSample {i+1}:")
            print(f"  Prompt:     '{prompt}'")
            print(f"  Reference:  '{reference_translation}'")
            print(f"  Model:      '{model_translation}'")
            print(f"  BLEU Score: {bleu_score:.4f}")

        except Exception as e:
            print(f"\nError processing sample {i+1}: {e}")

    average_bleu_score = total_blee_score / len(validation_data)
    print("\n--- Evaluation Complete ---")
    print(f"Average BLEU Score: {average_bleu_score:.4f}")
    print("Note: A higher BLEU score (closer to 1.0) indicates a better translation quality.")

if __name__ == "__main__":
    evaluate_model()