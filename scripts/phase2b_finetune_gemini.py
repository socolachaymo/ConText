# This script fine-tunes a Gemini model for translation.
# It uploads training and validation data, starts a fine-tuning job,
# and monitors its progress until completion.
import os
import google.generativeai as genai
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# --- API Key Validation Step ---
import subprocess
print("Validating API key with a direct curl request...")
validation_command = [
    "curl",
    "-H", "Content-Type: application/json",
    f"https://generativelanguage.googleapis.com/v1beta/models?key={GEMINI_API_KEY}"
]
try:
    result = subprocess.run(validation_command, capture_output=True, text=True, check=True)
    print("API key validation successful.")
except subprocess.CalledProcessError as e:
    print("\n--- API Key Validation Failed ---")
    print(f"Curl command failed with exit code {e.returncode}")
    print(f"Response: {e.stdout}")
    print("Please double-check your GEMINI_API_KEY in the .env file.")
    exit()
# --------------------------------

# Force the API key directly into the configuration
genai.configure(api_key=GEMINI_API_KEY)

def finetune_gemini_model():
    """
    Uploads the training data and starts a fine-tuning job on a Gemini model.
    """
    train_file_path = "data/train.jsonl"
    val_file_path = "data/validation.jsonl"
    model_display_name = "dialect-translator-gemini"

    if not os.path.exists(train_file_path) or not os.path.exists(val_file_path):
        print("Error: Training or validation file not found.")
        print("Please run split_dataset.py first.")
        return

    try:
        # 1. Start the fine-tuning job
        print("Starting new fine-tuning job...")
        tuned_model = genai.tuned_model.create(
            source_model="models/gemini-1.0-pro-001",
            training_data=train_file_path,
            validation_data=val_file_path,
            display_name=model_display_name,
            epoch_count=5,
        )

        print("\nFine-tuning job started successfully!")
        print(f"  Job Name: {tuned_model.name}")
        print(f"  Display Name: {tuned_model.display_name}")
        print(f"  State: {tuned_model.state}")

        # 2. Monitor the job
        print("\nMonitoring job status... (This may take a while)")
        while tuned_model.state != 'ACTIVE':
            time.sleep(60) # Wait for 1 minute before checking again
            tuned_model = genai.get_tuned_model(name=tuned_model.name)
            print(f"  Current State: {tuned_model.state} at {time.ctime()}")

        print("\n--- Fine-Tuning Complete! ---")
        print(f"Your fine-tuned model is now active.")
        print(f"Model Name: {tuned_model.name}")

    except Exception as e:
        print(f"An error occurred during the fine-tuning process: {e}")

if __name__ == "__main__":
    finetune_gemini_model()