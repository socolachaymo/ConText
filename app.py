import os
import subprocess
from flask import Flask, request, jsonify, send_from_directory
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from twelvelabs import TwelveLabs
from dotenv import load_dotenv
from werkzeug.utils import secure_filename

# --- Initialization ---
load_dotenv()
app = Flask(__name__, static_folder='frontend')

# Load Translation Model
model_path = "./results/final_model"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_path)

# Twelve Labs Client
api_key = os.getenv("TWELVE_LABS_API_KEY")
if not api_key:
    raise ValueError("TWELVE_LABS_API_KEY not found in .env file")
client = TwelveLabs(api_key=api_key)

# --- Helper Functions ---
def process_media(file_path, client):
    index_name = "dialect-translator-videos"
    indexes = client.index.list()
    index = next((i for i in indexes if i.name == index_name), None)
    if not index:
        index = client.index.create(name=index_name, models=[{"name": "marengo2.7", "options": ["visual", "audio"]}])

    task = client.task.create(index_id=index.id, file=file_path, language="en")
    task.wait()
    
    transcript_data = client.task.transcription(task.id)
    transcript = " ".join([segment['text'] for segment in transcript_data])
    return transcript

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
    input_type = request.form.get('type')
    raw_transcript = ""
    
    try:
        if input_type == 'text':
            raw_transcript = request.form.get('text')
        elif input_type in ['audio', 'video', 'record']:
            file = request.files.get('file')
            if not file:
                return jsonify({"error": "No file provided."}), 400
            
            upload_folder = 'temp_uploads'
            os.makedirs(upload_folder, exist_ok=True)
            filename = secure_filename(file.filename)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            
            raw_transcript = process_media(file_path, client)
            os.remove(file_path) # Clean up the uploaded file
        else:
            return jsonify({"error": "Invalid input type."}), 400

        if not raw_transcript:
            return jsonify({"error": "Could not extract text from input."}), 400

        translated_text = translate_text(raw_transcript, model, tokenizer)
        
        # For simplicity, we're not generating audio in this version.
        # You can integrate a TTS service here if needed.
        audio_url = None 

        return jsonify({
            "original": raw_transcript,
            "translated": translated_text,
            "audioUrl": audio_url
        })

    except Exception as e:
        print(f"Error during translation: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)