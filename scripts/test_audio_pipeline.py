# This script provides a pipeline for transcribing a video file using Twelve Labs.
# It uploads a video, waits for it to be processed, and then prints the raw transcript.
import os
import argparse
from dotenv import load_dotenv
from twelvelabs import TwelveLabs

def process_media(file_path, client):
    """
    Processes a video file with Twelve Labs to get the transcript,
    using the correct wait method from the documentation.
    """
    index_name = "dialect-translator-audio-test"
    indexes = client.index.list()
    index = next((i for i in indexes if i.name == index_name), None)
    if not index:
        print(f"Creating index '{index_name}'...")
        index = client.index.create(name=index_name, models=[{"name": "marengo2.7", "options": ["audio"]}])

    print("Uploading and processing video...")
    task = client.task.create(index_id=index.id, file=file_path, language="en")
    print(f"Task created with ID: {task.id}. Waiting for completion...")
    
    # Use the wait_for_done method as shown in the documentation
    task.wait_for_done(sleep_interval=5, callback=lambda t: print(f"  Status={t.status}"))

    if task.status != "ready":
        raise RuntimeError(f"Indexing failed with status {task.status}")

    print("Task complete. Retrieving transcript...")
    transcription = client.task.transcription(task.id)
    
    transcript_text = " ".join([segment.text for segment in transcription])
    return transcript_text

def main():
    parser = argparse.ArgumentParser(description="Transcribe a video file using Twelve Labs.")
    parser.add_argument("--api-key", help="Your Twelve Labs API key. If not provided, it will be read from the .env file.")
    args = parser.parse_args()

    # Determine API Key
    api_key = args.api_key
    if not api_key:
        load_dotenv()
        api_key = os.getenv("TWELVE_LABS_API_KEY")
    
    if not api_key:
        raise ValueError("API key not found. Provide it via the --api-key argument or in a .env file as TWELVE_LABS_API_KEY.")

    client = TwelveLabs(api_key=api_key.strip())
    
    video_file = "temp_videos/recorded_video.mp4"

    print(f"\nTranscribing {video_file}...")
    try:
        transcript = process_media(video_file, client)
        print("\n--- RAW TRANSCRIPT ---")
        print(transcript)
        print("----------------------")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()
