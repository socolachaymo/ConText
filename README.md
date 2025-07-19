# ConText: Dialect-Aware Translation and Audio Synthesis

ConText is a powerful tool that translates Caribbean dialect into standard English and generates high-quality audio of the translation. This project leverages a custom-trained language model combined with Google's Gemini for validation, ensuring accurate and nuanced translations.

## Features

-   **Video/Audio Transcription**: Ingests video data using Twelve Labs to extract dialectal speech.
-   **Custom LLM Translation**: Uses a fine-tuned GPT-3.5 Turbo model to translate Caribbean dialect to standard English.
-   **Gemini Validation**: Employs Gemini 1.5 Flash to review and refine the translation for accuracy and natural phrasing.
-   **Text-to-Speech**: Generates high-quality audio of the final translation using ElevenLabs.
-   **Web Interface**: A simple frontend to input dialectal phrases and receive the translated text and audio.

## Project Workflow

1.  **Data Ingestion & Preparation**:
    -   `phase1_data_ingestion.py`: Scrapes video URLs using Twelve Labs to get raw dialect transcripts.
    -   `phase1b_prepare_training_data.py`: Processes the raw transcripts through a robust translation pipeline (Gemini + GPT-4o) to create a high-quality `(dialect, standard_english)` dataset (`training_data.jsonl`).

2.  **Model Fine-Tuning**:
    -   `phase2b_finetune_llm.py`: Uploads the training data to OpenAI and starts a fine-tuning job on `gpt-3.5-turbo`.

3.  **Translation & Synthesis**:
    -   `app.py`: A Flask web server that exposes a translation API.
    -   The user inputs a dialect phrase in the frontend.
    -   The backend calls `phase2c_custom_translation_agent.py`, which:
        1.  Gets an initial translation from the fine-tuned model.
        2.  Uses Gemini to validate and correct the translation.
    -   The final, validated text is sent to `phase4_audio_reoutput.py` to generate an MP3 file using ElevenLabs.
    -   The frontend receives the translated text and a link to the audio file.

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
    ELEVENLABS_API_KEY="your_elevenlabs_api_key"
    ```

## How to Run

### Step 1: Scrape Video URLs

1.  (Optional) If you want to use a different channel, open `scripts/get_channel_videos.py` and change the `CHANNEL_URL` variable.
2.  Run the scraping script to gather all video URLs from the channel:
    ```bash
    python scripts/get_channel_videos.py
    ```
    This will create `data/video_urls.txt`.

### Step 2: Prepare Training Data

1.  Run the data ingestion script to download and transcribe the videos:
    ```bash
    python scripts/phase1_data_ingestion.py
    ```
2.  Run the data preparation script to create the high-quality training file:
    ```bash
    python scripts/phase1b_prepare_training_data.py
    ```
3.  Split the dataset into training and validation sets:
    ```bash
    python scripts/split_dataset.py
    ```
    This will create `data/train.jsonl` and `data/validation.jsonl`.

### Step 3: Fine-Tune the Gemini Model

1.  Run the fine-tuning script:
    ```bash
    python scripts/phase2b_finetune_gemini.py
    ```
2.  This script will monitor the job and let you know when it's complete. Once finished, copy the new model name (e.g., `tunedModels/dialect-translator-gemini-...`).

### Step 4: Evaluate Model Accuracy

1.  Open `scripts/evaluate_model.py` and update the `CUSTOM_MODEL_NAME` variable with your new fine-tuned model name.
2.  Run the evaluation script:
    ```bash
    python scripts/evaluate_model.py
    ```
    This will output the BLEU score, indicating the model's performance on the validation data.

### Step 5: Update and Run the Application

1.  Open `scripts/phase2c_custom_translation_agent.py` and update the `CUSTOM_MODEL_NAME` variable with your new fine-tuned model name.
2.  Run the Flask application:
    ```bash
    python app.py
    ```
3.  Open your browser and navigate to `http://127.0.0.1:5000`. You can now use the application to translate dialect phrases.