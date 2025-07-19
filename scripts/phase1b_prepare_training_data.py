import json
import os
from phase3_feedback_loop import run_feedback_loop

def prepare_training_data():
    """
    Loads dialect segments, translates them using the full feedback loop,
    and saves them as a structured dataset for LLM fine-tuning.
    """
    input_path = "data/segments.json"
    output_path = "data/training_data.jsonl"

    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        print("Please run phase1_data_ingestion.py first.")
        return

    with open(input_path, "r") as f:
        segments = json.load(f)

    print(f"Found {len(segments)} segments to process.")

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f_out:
        for i, segment in enumerate(segments):
            dialect_text = segment.get("text")
            if not dialect_text:
                continue

            print(f"\n--- Processing segment {i+1}/{len(segments)} ---")
            
            # Get the high-quality translation
            standard_english_text = run_feedback_loop(dialect_text)

            if "Error:" not in standard_english_text:
                # Create a JSON object for the training pair in the format required by Gemini
                training_pair = {
                    "input_text": f"Translate the following Caribbean dialect phrase to standard English: \"{dialect_text}\"",
                    "output_text": standard_english_text
                }
                
                # Write the JSON object as a new line in the output file
                f_out.write(json.dumps(training_pair) + "\n")
                print(f"  Saved training pair to {output_path}")
            else:
                print(f"  Skipping segment due to translation error.")

    print(f"\nTraining data preparation complete. Saved to {output_path}")

if __name__ == "__main__":
    prepare_training_data()