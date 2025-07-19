import json
import os
from sklearn.model_selection import train_test_split

def split_dataset(input_path="data/training_data.jsonl", test_size=0.2):
    """
    Splits the training data into a training set and a validation set.

    Args:
        input_path (str): Path to the full training_data.jsonl file.
        test_size (float): The proportion of the dataset to allocate to the validation set.
    """
    output_train_path = "data/train.jsonl"
    output_val_path = "data/validation.jsonl"

    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        print("Please run phase1b_prepare_training_data.py first.")
        return

    with open(input_path, "r") as f:
        data = [json.loads(line) for line in f]

    if len(data) < 2:
        print("Error: Not enough data to split. You need at least 2 samples.")
        return

    # Split the data
    train_data, val_data = train_test_split(data, test_size=test_size, random_state=42)

    # Save the training set
    with open(output_train_path, "w") as f:
        for item in train_data:
            f.write(json.dumps(item) + "\n")
    print(f"Training set saved to {output_train_path} ({len(train_data)} samples)")

    # Save the validation set
    with open(output_val_path, "w") as f:
        for item in val_data:
            f.write(json.dumps(item) + "\n")
    print(f"Validation set saved to {output_val_path} ({len(val_data)} samples)")

if __name__ == "__main__":
    split_dataset()