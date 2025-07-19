import subprocess
import os

# --- Configuration ---
# The URL of the YouTube channel you want to scrape.
CHANNEL_URL = "https://www.youtube.com/c/WhatYuhKnow"
# The file where the video URLs will be saved.
OUTPUT_FILE = "data/video_urls.txt"

def get_video_urls_from_channel(channel_url, output_file):
    """
    Uses yt-dlp to extract all video URLs from a YouTube channel.

    Args:
        channel_url (str): The URL of the YouTube channel.
        output_file (str): The path to the file to save the URLs in.
    """
    print(f"Fetching video URLs from channel: {channel_url}")
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    try:
        # Command to run yt-dlp
        # --flat-playlist: Do not extract video information, just list them.
        # --get-url: Print the URL of each video.
        command = [
            "yt-dlp",
            "--flat-playlist",
            "--get-url",
            channel_url
        ]

        # Run the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        video_urls = result.stdout.strip().split('\n')

        with open(output_file, "w") as f:
            for url in video_urls:
                f.write(url + "\n")

        print(f"\nSuccessfully saved {len(video_urls)} video URLs to {output_file}")
        print("You can now run the data ingestion script.")

    except FileNotFoundError:
        print("\nError: 'yt-dlp' command not found.")
        print("Please ensure yt-dlp is installed. You can install it with:")
        print("  pip install yt-dlp")
    except subprocess.CalledProcessError as e:
        print(f"\nAn error occurred while running yt-dlp:")
        print(e.stderr)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    get_video_urls_from_channel(CHANNEL_URL, OUTPUT_FILE)