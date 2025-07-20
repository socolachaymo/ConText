import os
from twelvelabs import TwelveLabs
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize TwelveLabs client
API_KEY = os.getenv("TWELVE_LABS_API_KEY")
if not API_KEY:
    raise ValueError("TWELVE_LABS_API_KEY not found in .env file")
client = TwelveLabs(api_key=API_KEY)

def transcribe_video(video_path):
    """Uploads video to Twelve Labs and returns transcript"""
    print("Uploading for transcription...")
    
    index_name = "hacking7"
    indexes = client.index.list()
    index = next((i for i in indexes if i.name == index_name), None)

    if not index:
        print(f"Creating new index: {index_name}")
        models = [
                {
                "name": "pegasus1",
                "options": ["visual", "audio"]
                }
        ]
        index = client.index.create(
            models=models,
            name=index_name
        )

    with open(video_path, "rb") as f:
        task = client.task.create(
            index_id=index.id,
            file=f
        )
    
    print(f"Task ID: {task.id} - Waiting for processing...")
    def on_task_update(task):
        print(f"  Status={task.status}")
    task.wait_for_done(sleep_interval=5, callback=on_task_update)
    if task.status != "ready":
        raise RuntimeError(f"Indexing failed with status {task.status}")
    print(f"The unique identifier of your video is {task.video_id}.")

    
    # transcript = client.task.transcription(task.id)
    prompt = "Generate a verbatim transcript for this video."
        
    res = client.generate.text(video_id=task.video_id, prompt=prompt, temperature=0.25)
    
    if res:
        return res.data
    return None

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Transcribe a video using Twelve Labs.")
    parser.add_argument("video_path", help="Path to the video file.")
    args = parser.parse_args()

    transcript = transcribe_video(args.video_path)
    if transcript:
        print("\nTranscript:")
        print(transcript)