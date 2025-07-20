# This script provides a command-line interface to translate a single
# Caribbean dialect phrase to standard English using the fine-tuned model.
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import argparse

def translate_with_custom_model(input_text):
    """
    Translates a given dialect phrase to standard English using the fine-tuned model.
    """
    model_path = "./results/final_model"
    
    try:
        # Load the fine-tuned model and tokenizer
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
        
        # Prepare the input text with the same prompt used during training
        prompt = f"Translate the following Caribbean dialect phrase to standard English: \"{input_text}\""
        inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=128)

        # Generate the translation
        output_sequences = model.generate(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            max_length=50,
            num_beams=5,  # Beam search for better quality
            early_stopping=True
        )
        
        # Decode the output
        translation = tokenizer.decode(output_sequences[0], skip_special_tokens=True)

        return translation.strip()

    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Translate dialect to standard English using a custom fine-tuned model.")
    parser.add_argument("dialect_phrase", type=str, help="The Caribbean dialect phrase to translate.")
    args = parser.parse_args()
    
    translation = translate_with_custom_model(args.dialect_phrase)
    print(f"\nDialect Phrase: {args.dialect_phrase}")
    print(f"Standard English Translation: {translation}")
    
