import os
import json
import cv2
import time
from twelvelabs import TwelveLabs
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize TwelveLabs client
API_KEY = os.getenv("TWELVE_LABS_API_KEY")
if not API_KEY:
    raise ValueError("TWELVE_LABS_API_KEY not found in .env file")
client = TwelveLabs(api_key=API_KEY)

def record_video(output_path="recording.mp4", duration=10):
    """
    Records video from webcam and saves to file
    :param duration: Recording time in seconds
    """
    cap = cv2.VideoCapture(0)  # 0 = default camera
    
    # Video writer setup
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (640, 480))
    
    print(f"Recording for {duration} seconds... (Press 'q' to stop early)")
    start_time = time.time()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        out.write(frame)
        cv2.imshow('Recording', frame)
        
        # Stop conditions
        if (time.time() - start_time) > duration:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"Recording saved to {output_path}")

def transcribe_video(video_path):
    """Uploads video to Twelve Labs and returns transcript"""
    print("Uploading for transcription...")
    
    with open(video_path, "rb") as f:
        models = [
                {
                "name": "pegasus1",  # Use Pegasus for generation capabilities
                "options": ["visual", "audio"]     
                }
        ]
        index = client.index.create(
            models=models,
            name="hacking7"
        )
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
    return res

if __name__ == "__main__":
    
    # Step 2: Transcribe
    result = transcribe_video("video.mp4")
    
    # Save results
    # with open("transcript.json", "w") as f:
    #     json.dump(segments, f, indent=2)
    
    print("\nTranscript:")
    # for segment in segments:
    #     print(f"{segment['timestamp']}: {segment['text']}")
    if result:
        print(result.data)