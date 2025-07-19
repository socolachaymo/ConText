import os
import json
from twelvelabs import TwelveLabs
from dotenv import load_dotenv

load_dotenv()

# Initialize TwelveLabs client
API_KEY = os.getenv("TWELVE_LABS_API_KEY")
if not API_KEY:
    raise ValueError("TWELVE_LABS_API_KEY not found in .env file")

client = TwelveLabs(api_key=API_KEY)

def load_video_urls(file_path="data/video_urls.txt"):
    """Loads video URLs from a text file."""
    if not os.path.exists(file_path):
        print(f"URL file not found at {file_path}.")
        print("Please run 'get_channel_videos.py' first to generate the URL list.")
        return []
    with open(file_path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def process_videos(video_urls):
    """
    Uploads videos to Twelve Labs, waits for indexing,
    and extracts speech segments.
    """
    all_segments = []

    for url in video_urls:
        print(f"Processing video: {url}")

        # Upload video from URL
        task = client.tasks.create(url=url, language="en")
        print(f"  Task created with ID: {task.id}")

        # Wait for indexing to complete
        task.wait()
        print(f"  Video indexed successfully.")

        # Get transcript
        transcript = client.tasks.transcription(task.id)

        # Store segments
        for segment in transcript:
            all_segments.append({
                "timestamp": segment.start,
                "dialect": "unknown",  # To be manually annotated
                "audio_url": url,
                "text": segment.text,
            })

    # Save to JSON file
    with open("data/segments.json", "w") as f:
        json.dump(all_segments, f, indent=2)

    print("\nAll videos processed. Segments saved to data/segments.json")

if __name__ == "__main__":
    video_urls = load_video_urls()
    if video_urls:
        print(f"Found {len(video_urls)} URLs to process.")
        process_videos(video_urls)
    else:
        print("No video URLs to process. Exiting.")