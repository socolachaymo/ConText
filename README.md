# ConText: Dialect-Aware Translation and Audio Synthesis

ConText is a powerful tool that translates dialect into standard English and generates high-quality text  of the translation. This project leverages a custom-trained language model combined with Google's Gemini for validation, ensuring accurate and nuanced translations.

## Features

-   **Video/Audio Transcription**: Ingests video data using Twelve Labs to extract speech.
-   **Custom LLM Translation**: Uses a fine-tuned T5 model to translate dialect to standard English.
-   **Text-to-Speech**: Generates high-quality audio of the final translation.
-   **Web Interface**: A simple frontend to input dialectal phrases and receive the translated text and audio.

## Project Workflow

The project is divided into several scripts, each responsible for a specific part of the workflow.

### Data Collection and Preparation

2.  **`get_youtube_comments.py`**: Fetches comments from a list of specified YouTube channels using the YouTube Data API.
4.  **`translate_new_data.py`**: Uses a fine-tuned translation model to generate draft translations for a new dataset of comments.
5.  **`merge_datasets.py`**: Merges the original dataset with a new dataset of translated comments to create an augmented dataset.
6.  **`phase1b_prepare_training_data.py`**: Prepares the training data for the translation model by converting a CSV file of dialect and standard English pairs into a JSONL file.
7.  **`split_dataset.py`**: Splits the training data into a training set and a validation set.

### Model Training and Evaluation

8.  **`phase2b_finetune_llm.py`**: Fine-tunes a T5 model for translation using the Hugging Face Transformers library.
10. **`evaluate_model.py`**: Evaluates the fine-tuned translation model using the BLEU score.

### Audio and Video Tools

11. **`record_audio.py`**: Records audio from the microphone.
12. **`record_video.py`**: Records a video from the default camera.
13. **`convert_audio_to_video.py`**: Converts an audio file to a video file with a black screen.
14. **`test_audio_pipeline.py`**: A pipeline for transcribing a video file using Twelve Labs (still has to be fixed).

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd ConText
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r scripts/requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory and add your API keys:
    ```
    TWELVE_LABS_API_KEY="your_twelve_labs_api_key"
    GEMINI_API_KEY="your_gemini_api_key"
    ```

## How to Run the Scripts

Each script can be run independently. Here is a typical workflow:

### Step 1: Collect Data

1.  **Fetch Video URLs**: (Just use comments for now)
     ```bash
    python scripts/get_channel_videos.py
    ```
2.  **Fetch YouTube Comments**:
    ```bash
    python scripts/get_youtube_comments.py
    ```

### Step 2: Process Data and Prepare for Training

1.  **Ingest Videos**:
    ```bash
    python scripts/phase1_data_ingestion.py
    ```
2.  **Translate New Comments**:
    ```bash
    python scripts/translate_new_data.py
    ```
3.  **Merge Datasets**:
    ```bash
    python scripts/merge_datasets.py
    ```
4.  **Prepare Training Data**:
    ```bash
    python scripts/phase1b_prepare_training_data.py
    ```
5.  **Split Dataset**:
    ```bash
    python scripts/split_dataset.py
    ```

### Step 3: Fine-Tune and Evaluate a Model

1.  **Fine-Tune a T5 Model**:
    ```bash
    python scripts/phase2b_finetune_llm.py
    ```
2.  **Evaluate the Model**:
    ```bash
    python scripts/evaluate_model.py
    ```

### Step 4: Run the Application

1.  **Run the Flask application**:
    ```bash
    python app.py
    ```
