# This script ingests videos from a list of URLs into Twelve Labs for analysis.
# It downloads each video, uploads it to Twelve Labs, and extracts the transcript.
import os
import subprocess
import json
import argparse
from twelvelabs import TwelveLabs
from dotenv import load_dotenv

def load_video_urls(file_path="data/video_urls.txt"):
    """Loads video URLs from a text file."""
    if not os.path.exists(file_path):
        print(f"URL file not found at {file_path}.")
        print("Please run 'get_channel_videos.py' first to generate the URL list.")
        return []
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def get_or_create_index(client, index_name="dialect-translator-videos"):
    """Gets an existing index by name or creates a new one."""
    indexes = client.index.list()
    for index in indexes:
        if index.name == index_name:
            print(f"Found existing index: {index_name} (ID: {index.id})")
            return index.id
    
    print(f"Index '{index_name}' not found. Creating a new one...")
    index = client.index.create(name=index_name, models=[{"name": "marengo2.7", "options": ["visual", "audio"]}])
    print(f"Successfully created index: {index_name} (ID: {index.id})")
    return index.id

def process_videos(video_urls, index_id):
    """
    Uploads videos to Twelve Labs, waits for indexing,
    and extracts speech segments.
    """
    all_segments = []

    for i, url in enumerate(video_urls):
        print(f"\n--- Processing video {i+1}/{len(video_urls)}: {url} ---")
        temp_video_path = None
        try:
            # 1. Download video locally using yt-dlp
            print("  Downloading video locally...")
            video_filename = f"temp_videos/video_{i+1}.mp4"
            download_command = ["yt-dlp", "-o", video_filename, url]
            subprocess.run(download_command, check=True, capture_output=True)
            temp_video_path = video_filename
            print(f"  Video downloaded to {temp_video_path}")

            # 2. Upload the local file to Twelve Labs
            print("  Uploading video file to Twelve Labs...")
            task = client.task.create(index_id=index_id, file=temp_video_path, language="en")
            print(f"  Task created with ID: {task.id}")

            # 3. Wait for indexing
            print("  Waiting for video to be indexed...")
            task.wait()
            print(f"  Video indexed successfully.")

            # 4. Get transcript
            transcript = client.task.transcription(task.id)

            # 5. Store segments
            for segment in transcript:
                all_segments.append({
                    "timestamp": segment.start,
                    "dialect": "unknown",
                    "original_url": url,
                    "text": segment.text,
                })
            print(f"  Successfully processed and transcribed video.")

        except subprocess.CalledProcessError as e:
            print(f"  Failed to download video from URL: {url}")
            print(f"  Yt-dlp Error: {e.stderr.decode()}")
        except Exception as e:
            print(f"  An unexpected error occurred while processing {url}")
            print(f"  Error: {e}")
        finally:
            # 6. Clean up the temporary file
            if temp_video_path and os.path.exists(temp_video_path):
                os.remove(temp_video_path)
                print(f"  Cleaned up temporary file: {temp_video_path}")

    # Save to JSON file
    with open("data/segments.json", "w") as f:
        json.dump(all_segments, f, indent=2)

    print("\nVideo processing complete. Segments saved to data/segments.json")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest videos into Twelve Labs.")
    parser.add_argument("--api-key", help="Your Twelve Labs API key. Overrides the .env file.")
    args = parser.parse_args()

    # Determine API Key
    api_key = args.api_key
    if not api_key:
        load_dotenv()
        api_key = os.getenv("TWELVE_LABS_API_KEY")
    
    if api_key:
        api_key = api_key.strip()

    if not api_key:
        raise ValueError("API key not found. Provide it via --api-key or in a .env file as TWELVE_LABS_API_KEY.")

    client = TwelveLabs(api_key=api_key)

    video_urls = load_video_urls()
    if video_urls:
        print(f"Found {len(video_urls)} URLs to process.")
        try:
            index_id = get_or_create_index(client)
            process_videos(video_urls, index_id)
        except Exception as e:
            print(f"\nAn error occurred: {e}")
            print("Please double-check your API key and ensure it is valid.")
    else:
        print("No video URLs to process. Exiting.")