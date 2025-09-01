# This script fetches comments from a list of specified YouTube channels
# using the YouTube Data API. It saves the comments to a CSV file.
import requests
import csv
import argparse
import os
from dotenv import load_dotenv

def get_youtube_comments(api_key):
    """
    Fetches comments from specified YouTube channels and saves them to a CSV file.
    """
    # Channel names (change these as needed)
    CHANNEL_NAMES = ['WhatYuhKnow', 'MachelMontano', 'BujuBanton', 'Aytian']
    BASE_URL = 'https://www.googleapis.com/youtube/v3/'

    def get_channel_id(channel_name, api_key):
        url = f"{BASE_URL}search?part=snippet&type=channel&q={channel_name}&key={api_key}"
        response = requests.get(url).json()
        if 'items' in response and len(response['items']) > 0:
            return response['items'][0]['id']['channelId']
        else:
            print(f"No channel found for {channel_name}")
            return None

    def get_videos(channel_id, api_key):
        url = f"{BASE_URL}search?part=id&channelId={channel_id}&maxResults=50&order=date&type=video&key={api_key}"
        response = requests.get(url).json()
        return [item['id']['videoId'] for item in response.get('items', [])]

    def get_comments(video_id, api_key):
        url = f"{BASE_URL}commentThreads?part=snippet&videoId={video_id}&key={api_key}"
        response = requests.get(url).json()
        return [item['snippet']['topLevelComment']['snippet']['textOriginal'] for item in response.get('items', [])]

    all_comments = []
    for channel_name in CHANNEL_NAMES:
        print(f"Fetching comments from {channel_name}...")
        channel_id = get_channel_id(channel_name, api_key)
        if channel_id:
            videos = get_videos(channel_id, api_key)
            for video in videos:
                comments = get_comments(video, api_key)
                all_comments.extend(comments)

    output_file = 'youtube_comments.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Comment'])  # Header row
        for comment in all_comments:
            writer.writerow([comment])

    print(f"\nSaved {len(all_comments)} comments to '{output_file}'")

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise ValueError("API key not found. Provide it in a .env file as YOUTUBE_API_KEY.")
    get_youtube_comments(api_key)
