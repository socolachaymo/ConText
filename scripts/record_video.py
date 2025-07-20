# This script records a video from the default camera for a specified duration.
# It saves the recording as an MP4 file.
import cv2
import argparse
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

    print(f"Recording for {duration} seconds... Press 'q' to stop early.")
    
    start_time = time.time()
    while (time.time() - start_time) < duration:
        ret, frame = cap.read()
        if ret:
            out.write(frame)
            cv2.imshow('Recording...', frame)
            
            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
            
    # Release everything when the job is done
    cap.release()
    out.release()
    cv2.destroyAllWindows()
    
    print(f"Video saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Record a video from the default camera.")
    parser.add_argument("output_file", help="Path to save the recorded video file (e.g., temp_videos/my_video.mp4).")
    parser.add_argument("--duration", type=int, default=10, help="Duration of the recording in seconds.")
    args = parser.parse_args()

    record_video(args.output_file, args.duration)