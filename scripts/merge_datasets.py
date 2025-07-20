# This script merges the original dataset with a new dataset of translated comments.
# It creates an augmented dataset for training the translation model.
import pandas as pd
import os

def merge_datasets():
    """
    Merges the original dataset.csv with the newly translated youtube_comments.csv.
    """
    # Define file paths
    original_dataset_path = 'dataset.csv'
    new_dataset_path = 'translated_youtube_comments.csv'
    output_path = 'augmented_dataset.csv'

    # Check if files exist
    if not os.path.exists(original_dataset_path):
        print(f"Error: {original_dataset_path} not found.")
        return
    if not os.path.exists(new_dataset_path):
        print(f"Error: {new_dataset_path} not found.")
        return

    # Read the datasets
    print("Reading datasets...")
    original_df = pd.read_csv(original_dataset_path)
    new_df = pd.read_csv(new_dataset_path)

    # Standardize column names if they are different, assuming 'prompt' and 'response'
    original_df.columns = ['prompt', 'response']
    new_df.columns = ['prompt', 'response']

    # Concatenate the dataframes
    print("Merging datasets...")
    merged_df = pd.concat([original_df, new_df], ignore_index=True)

    # Drop rows with missing values
    merged_df.dropna(inplace=True)

    # Remove duplicates
    merged_df.drop_duplicates(inplace=True)

    # Save the merged dataset
    print(f"Saving merged dataset to {output_path}...")
    merged_df.to_csv(output_path, index=False)
    print("Merge complete.")
    print(f"Original dataset size: {len(original_df)}")
    print(f"New data size: {len(new_df)}")
    print(f"Total augmented dataset size: {len(merged_df)}")

if __name__ == "__main__":
    merge_datasets()