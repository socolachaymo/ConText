# ConText: Dialect-Aware Translation and Audio Synthesis

ConText is a powerful tool that translates dialect into standard English and generates high-quality audio of the translation. This project leverages a custom-trained language model combined with Google's Gemini for validation, ensuring accurate and nuanced translations.

## Features

-   **Video/Audio Transcription**: Ingests video data using Twelve Labs to extract dialectal speech.
-   **Custom LLM Translation**: Uses a fine-tuned T5 model to translate dialect to standard English.
-   **Text-to-Speech**: Generates high-quality audio of the final translation.
-   **Web Interface**: A simple frontend to input dialectal phrases and receive the translated text and audio.
    -   **File Upload**: Supports both audio and video file uploads.
    -   **Live Recording**: Record video and audio directly in the browser.
    -   **Clear Button**: Easily clear the input and output fields.

## Project Workflow

The project is divided into several scripts, each responsible for a specific part of the workflow.

### Data Collection and Preparation

2.  **`get_youtube_comments.py`**: Fetches comments from a list of specified YouTube channels using the YouTube Data API.
3.  **`phase1_data_ingestion.py`**: Ingests videos from a list of URLs into Twelve Labs for analysis. It downloads each video, uploads it to Twelve Labs, and extracts the transcript.
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
14. **`test_audio_pipeline.py`**: A pipeline for transcribing a video file using Twelve Labs.

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

1.  **Fetch Video URLs**:
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

## Running the Application

To run the web application, you need to have the backend server running and the frontend built.

### 1. Build the Frontend

The frontend is a React application built with Vite. The Flask server is configured to serve the built frontend files.

1.  **Navigate to the frontend directory**:
    ```bash
    cd new_frontend
    ```
2.  **Install dependencies**:
    ```bash
    npm install
    ```
    or if you use bun:
    ```bash
    bun install
    ```
3.  **Build the frontend for production**:
    ```bash
    npm run build
    ```
    or
    ```bash
    bun run build
    ```
    This will create a `dist` directory in `new_frontend` with the static files. Once the build is complete, navigate back to the root directory:
    ```bash
    cd ..
    ```

### 2. Run the Backend Server

From the root directory of the project, run the Flask application:

```bash
python app.py
```

The backend server will start on `http://127.0.0.1:5002`.

### 3. Access the Application

Once the backend is running, open your browser and navigate to:

[http://127.0.0.1:5002](http://127.0.0.1:5002)

You can now use the application to translate dialect phrases by typing text, uploading an audio/video file, or recording a video directly in the browser.

### Where is the Translation Logic?

The core translation logic is not in a standalone script. It is handled within the Flask web server, **`app.py`**.

Specifically, the `translate_text()` function inside `app.py` takes the input text, uses the loaded fine-tuned model and tokenizer, and returns the standard English translation. The web interface is the primary way to interact with the translation model.

### Command-Line Translation

If you want to translate a single phrase from the command line, you can use the `phase2c_custom_translation_agent.py` script:

```bash
python3 scripts/phase2c_custom_translation_agent.py "Your dialect phrase here"
