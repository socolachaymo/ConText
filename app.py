import os
import subprocess
import time
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from scripts.transcribe_video import transcribe_video
from scripts.record_video import record_video
from scripts.convert_audio_to_video import convert_audio_to_video

# --- Initialization ---
load_dotenv()
app = Flask(__name__, static_folder='new_frontend/dist')
CORS(app)

# Load Translation Model
model_path = "./results/final_model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

def translate_text(text, model, tokenizer):
    prompt = f"Translate the following Caribbean dialect phrase to standard English: \"{text}\""
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    
    output_sequences = model.generate(
        input_ids=inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        max_length=100,
        num_beams=5,
        early_stopping=True
    )
    
    translation = tokenizer.decode(output_sequences[0], skip_special_tokens=True)
    return translation.strip()

# --- API Routes ---
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/translate', methods=['POST'])
def translate():
    data = request.form
    files = request.files
    raw_transcript = ""

    try:
        if 'text' in data:
            raw_transcript = data['text']
        elif 'file' in files:
            file = files['file']
            upload_folder = 'temp_uploads'
            os.makedirs(upload_folder, exist_ok=True)
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)

            if file.content_type.startswith('audio/'):
                video_path = os.path.join(upload_folder, f"{os.path.splitext(filename)[0]}.mp4")
                if convert_audio_to_video(file_path, video_path):
                    raw_transcript = transcribe_video(video_path)
                    os.remove(video_path)
                else:
                    os.remove(file_path)
                    return jsonify({"error": "Failed to convert audio to video."}), 500
            else:
                raw_transcript = transcribe_video(file_path)
            
            os.remove(file_path)
        else:
            return jsonify({"error": "No input provided."}), 400

        if not raw_transcript:
            return jsonify({"error": "Could not extract text from input."}), 400

        translated_text = translate_text(raw_transcript, model, tokenizer)
        
        return jsonify({
            "original": raw_transcript,
            "translated": translated_text,
        })

    except Exception as e:
        print(f"Error during translation: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/record', methods=['POST'])
def record_and_transcribe():
    try:
        output_folder = 'temp_recordings'
        os.makedirs(output_folder, exist_ok=True)
        video_path = os.path.join(output_folder, f"recording_{int(time.time())}.mp4")
        
        # Record video
        record_video(video_path, duration=10)
        
        # Transcribe video
        raw_transcript = transcribe_video(video_path)
        
        # Clean up the recorded file
        os.remove(video_path)
        
        if not raw_transcript:
            return jsonify({"error": "Could not transcribe the recording."}), 400
            
        # Translate the transcript
        translated_text = translate_text(raw_transcript, model, tokenizer)
        
        return jsonify({
            "original": raw_transcript,
            "translated": translated_text,
        })

    except Exception as e:
        print(f"Error during recording/transcription: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5002)