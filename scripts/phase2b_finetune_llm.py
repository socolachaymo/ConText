# This script fine-tunes a T5 model for translation using the Hugging Face Transformers library.
# It loads a pre-trained model, tokenizes the training and validation data,
# and then runs the training process, saving the final model.
import os
import json
import torch
from datasets import load_dataset
from transformers import (
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForSeq2Seq,
)

def fine_tune_custom_llm():
    """
    Fine-tunes a custom Language Model from Hugging Face.
    """
    # --- 1. Configuration ---
    model_name = "t5-base"  # A more powerful model for seq-to-seq tasks
    train_file = "data/train.jsonl"
    val_file = "data/validation.jsonl"
    output_dir = "./results"
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir=output_dir,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        per_device_eval_batch_size=4,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
        eval_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
    )

    # --- 2. Load and Prepare Data ---
    print("Loading and preparing dataset...")
    
    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # Load datasets from JSONL files
    data_files = {"train": train_file, "validation": val_file}
    raw_datasets = load_dataset('json', data_files=data_files)

    def tokenize_function(examples):
        # T5 uses a prefix for different tasks. We'll use the one from the prompt.
        inputs = examples["input_text"]
        targets = examples["output_text"]
        
        # Tokenize inputs and targets
        model_inputs = tokenizer(inputs, max_length=128, truncation=True, padding="max_length")
        labels = tokenizer(targets, max_length=128, truncation=True, padding="max_length")
        
        model_inputs["labels"] = labels["input_ids"]
        return model_inputs

    tokenized_datasets = raw_datasets.map(
        tokenize_function,
        batched=True,
        remove_columns=raw_datasets["train"].column_names,
    )

    # Data collator for sequence-to-sequence models
    data_collator = DataCollatorForSeq2Seq(
        tokenizer=tokenizer,
        model=model
    )

    # --- 3. Initialize Trainer ---
    print("Initializing Trainer...")
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets["train"],
        eval_dataset=tokenized_datasets["validation"],
        data_collator=data_collator,
    )

    # --- 4. Start Fine-Tuning ---
    print("Starting fine-tuning...")
    trainer.train()

    # --- 5. Save the Model ---
    print("Fine-tuning complete. Saving model...")
    model.save_pretrained(f"{output_dir}/final_model")
    tokenizer.save_pretrained(f"{output_dir}/final_model")
    
    print(f"Model saved to {output_dir}/final_model")

if __name__ == "__main__":
    fine_tune_custom_llm()