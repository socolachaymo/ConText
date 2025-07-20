# This script fetches video URLs from a specified YouTube channel using yt-dlp.
# It filters out YouTube Shorts and saves the URLs to a text file.
import subprocess
import os

# --- Configuration ---
# The URL of the YouTube channel you want to scrape.
CHANNEL_URL = "https://www.youtube.com/c/WhatYuhKnow"
# The file where the video URLs will be saved.
OUTPUT_FILE = "data/video_urls.txt"
VIDEO_LIMIT = 10

def get_video_urls_from_channel(channel_url, output_file, limit=None, timeout=60):
    """
    Uses yt-dlp to extract video URLs from a YouTube channel.

    Args:
        channel_url (str): The URL of the YouTube channel.
        output_file (str): The path to the file to save the URLs in.
        limit (int, optional): The maximum number of videos to fetch.
        timeout (int, optional): The timeout in seconds for the yt-dlp command.
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
        ]
        if limit:
            # Use yt-dlp to limit the number of videos fetched for efficiency
            command.extend(["--playlist-items", f"1-{limit}"])
        
        command.append(channel_url)

        # Run the command and capture the output
        result = subprocess.run(command, capture_output=True, text=True, check=True, timeout=timeout)
        
        video_urls = result.stdout.strip().split('\n')

        # Filter out YouTube Shorts
        filtered_urls = [url for url in video_urls if "watch?v=" in url]

        with open(output_file, "w") as f:
            for url in filtered_urls:
                f.write(url + "\n")

        print(f"\nSuccessfully saved {len(filtered_urls)} video URLs to {output_file}")
        print("You can now run the data ingestion script.")

    except FileNotFoundError:
        print("\nError: 'yt-dlp' command not found.")
        print("Please ensure yt-dlp is installed. You can install it with:")
        print("  pip install yt-dlp")
    except subprocess.TimeoutExpired:
        print(f"\nError: The command timed out after {timeout} seconds.")
        print("The channel might have too many videos or there could be a network issue.")
    except subprocess.CalledProcessError as e:
        print(f"\nAn error occurred while running yt-dlp:")
        print(e.stderr)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    get_video_urls_from_channel(CHANNEL_URL, OUTPUT_FILE, limit=VIDEO_LIMIT)