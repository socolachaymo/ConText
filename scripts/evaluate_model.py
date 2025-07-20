# This script evaluates the fine-tuned translation model using the BLEU score.
# It compares the model's translations against a validation set of reference translations.
import os
import json
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import json
import os

# --- Configuration ---
CUSTOM_MODEL_NAME = "./results/final_model"

def evaluate_model(validation_file="data/validation.jsonl"):
    """
    Evaluates the fine-tuned custom model against the validation set and calculates the BLEU score.
    """
    if not os.path.exists(CUSTOM_MODEL_NAME):
        print(f"Error: Model not found at {CUSTOM_MODEL_NAME}")
        return

    if not os.path.exists(validation_file):
        print(f"Error: Validation file not found at {validation_file}")
        return

    tokenizer = AutoTokenizer.from_pretrained(CUSTOM_MODEL_NAME)
    model = AutoModelForSeq2SeqLM.from_pretrained(CUSTOM_MODEL_NAME)
    
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
            inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
            output_sequences = model.generate(
                input_ids=inputs['input_ids'],
                attention_mask=inputs['attention_mask'],
                max_length=50,
                num_beams=5,
                early_stopping=True
            )
            model_translation = tokenizer.decode(output_sequences[0], skip_special_tokens=True).strip()

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

    average_bleu_score = total_bleu_score / len(validation_data)
    print("\n--- Evaluation Complete ---")
    print(f"Average BLEU Score: {average_bleu_score:.4f}")
    print("Note: A higher BLEU score (closer to 1.0) indicates a better translation quality.")

if __name__ == "__main__":
    evaluate_model()