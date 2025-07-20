# This script prepares the training data for the translation model.
# It converts a CSV file of dialect and standard English pairs into a
# JSONL file formatted for fine-tuning a large language model.
import json
import os
import csv
import json

def prepare_training_data_from_csv():
    """
    Loads dialect and standard English pairs from a CSV file
    and saves them as a structured dataset for LLM fine-tuning.
    """
    input_path = "augmented_dataset.csv"
    output_path = "data/training_data.jsonl"

    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        return

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        with open(input_path, "r", encoding="utf-8") as f_in, \
             open(output_path, "w") as f_out:
            
            reader = csv.reader(f_in)
            header = next(reader) # Skip header row
            
            print(f"Reading from {input_path} with header: {header}")
            
            count = 0
            for row in reader:
                if not row or len(row) < 2:
                    continue

                dialect_text = row[0].replace("tec:", "").strip()
                standard_english_text = row[1].strip()

                if not dialect_text or not standard_english_text:
                    continue

                # Create a JSON object for the training pair
                training_pair = {
                    "input_text": f"Translate the following Caribbean dialect phrase to standard English: \"{dialect_text}\"",
                    "output_text": standard_english_text
                }
                
                # Write the JSON object as a new line in the output file
                f_out.write(json.dumps(training_pair) + "\n")
                count += 1

        print(f"\nSuccessfully processed {count} training pairs.")
        print(f"Training data preparation complete. Saved to {output_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    prepare_training_data_from_csv()