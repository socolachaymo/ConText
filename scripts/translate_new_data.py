# This script uses a fine-tuned translation model to generate draft translations
# for a new dataset of comments. The output is a CSV file with prompts and responses.
import csv
import os
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

def translate_new_data():
    """
    Uses the current fine-tuned model to create draft translations for a new dataset.
    """
    input_file = 'youtube_comments.csv'
    output_file = 'translated_youtube_comments.csv'
    model_path = "./results/final_model"

    if not os.path.exists(input_file):
        print(f"Error: Input file not found at {input_file}")
        return

    print("Loading translation model...")
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

    def translate_text(text):
        prompt = f"Translate the following Caribbean dialect phrase to standard English: \"{text}\""
        inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
        
        output_sequences = model.generate(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            max_length=100,
            num_beams=5,
            early_stopping=True
        )
        
        return tokenizer.decode(output_sequences[0], skip_special_tokens=True).strip()

    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', newline='', encoding='utf-8') as f_out:
        
        reader = csv.reader(f_in)
        writer = csv.writer(f_out)
        
        header = next(reader)  # Skip header
        writer.writerow(['prompt', 'response'])  # Write new header

        print(f"Translating comments from {input_file}...")
        for i, row in enumerate(reader):
            dialect_comment = row[0]
            
            # Add the required prefix to the prompt
            prompt_text = f"tec:{dialect_comment}"
            
            # Get the draft translation
            draft_translation = translate_text(dialect_comment)
            
            writer.writerow([prompt_text, draft_translation])
            
            if (i + 1) % 10 == 0:
                print(f"  ...translated {i + 1} comments")

    print(f"\nDraft translations saved to {output_file}")
    print("Please review and correct the translations in this file before retraining the model.")

if __name__ == "__main__":
    translate_new_data()