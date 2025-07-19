import os
from elevenlabs import generate, play, set_api_key
from dotenv import load_dotenv
from phase2c_custom_translation_agent import run_custom_translation_pipeline

load_dotenv()

# Configure ElevenLabs API
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not ELEVENLABS_API_KEY:
    raise ValueError("ELEVENLABS_API_KEY not found in .env file")

set_api_key(ELEVENLABS_API_KEY)

def text_to_speech(text: str, filename: str):
    """
    Converts text to speech using ElevenLabs and saves it to a file.
    """
    try:
        # Generate audio
        audio = generate(
            text=text,
            voice="Rachel",  # You can choose a different voice
            model="eleven_multilingual_v2"
        )

        # Save audio to file
        with open(filename, "wb") as f:
            f.write(audio)

        print(f"Audio saved to {filename}")
        # play(audio) # Uncomment to play audio automatically
        return filename
    except Exception as e:
        print(f"An error occurred during text-to-speech conversion: {e}")
        return None

if __name__ == "__main__":
    # Example usage:
    dialect_phrase = "Mi glad fi see yuh."

    # Get the validated translation from the feedback loop
    validated_translation = run_custom_translation_pipeline(dialect_phrase)

    if validated_translation and "Error:" not in validated_translation:
        print(f"\n--- Generating Audio for: '{validated_translation}' ---")
        # Generate a unique filename
        output_filename = f"output_audio/translated_{dialect_phrase.replace(' ', '_').lower()}.mp3"
        text_to_speech(validated_translation, output_filename)
    else:
        print("\nCould not generate audio due to translation error.")