from flask import Flask, request, jsonify, send_from_directory
from scripts.phase2c_custom_translation_agent import run_custom_translation_pipeline
from scripts.phase4_audio_reoutput import text_to_speech
import os

app = Flask(__name__, static_folder='frontend')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/translate', methods=['POST'])
def translate():
    data = request.get_json()
    dialect_text = data.get('text')

    if not dialect_text:
        return jsonify({'error': 'No text provided'}), 400

    # Get the translation
    translated_text = run_custom_translation_pipeline(dialect_text)
    if "Error:" in translated_text:
        return jsonify({'error': translated_text}), 500

    # Generate the audio
    output_filename = f"output_audio/translated_{dialect_text.replace(' ', '_').lower()}.mp3"
    audio_path = text_to_speech(translated_text, output_filename)
    if not audio_path:
        return jsonify({'error': 'Failed to generate audio'}), 500

    return jsonify({
        'translated': translated_text,
        'audioUrl': f'/{audio_path}'
    })

if __name__ == '__main__':
    # Ensure the output directory exists
    os.makedirs('output_audio', exist_ok=True)
    app.run(debug=True, port=5000)