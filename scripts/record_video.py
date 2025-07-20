# This script records a video from the default camera for a specified duration.
# It saves the recording as an MP4 file.
import cv2
import time

def record_video(output_file, duration=10):
    """
    Records a video from the default camera for a specified duration.
    """
    # Open the default camera
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Get the camera's frame width and height
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, 20.0, (frame_width, frame_height))

    print(f"Recording for {duration} seconds...")
    
    start_time = time.time()
    while (time.time() - start_time) < duration:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
        else:
            break
            
    # Release everything when the job is done
    cap.release()
    out.release()
    
    print(f"Video saved to {output_file}")