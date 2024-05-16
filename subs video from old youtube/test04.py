"""
This script utilizes the video data stored in "output1.json" to download thumbnails and videos from YouTube. Each video's title is used to create a directory within the 'videos' folder, where the thumbnail image and video file are saved.

For each video:
1. It fetches the thumbnail URL using PyTube library.
2. Creates a directory for the video if it doesn't exist.
3. Downloads the thumbnail image and saves it as "{title}.jpg" in the video's directory.
4. Attempts to download the video itself using PyTube's first available stream.

If a video is age-restricted or unavailable, it skips downloading and prints the corresponding error message.

Ensure that PyTube and requests libraries are installed and accessible to run this script successfully.
"""

import os
import json
from pytube import YouTube
from pytube.exceptions import AgeRestrictedError, VideoUnavailable
import requests

# Load video data from JSON file
with open("output1.json", "r") as json_file:
    videos = json.load(json_file)

# Loop through the list of videos and download each thumbnail
for video in videos:
    title = video["title"]
    link = video["link"]

    try:
        # Get thumbnail URL using pytube
        yt = YouTube(link)
        thumbnail_url = yt.thumbnail_url

        # Create videos directory if it doesn't exist
        if not os.path.exists('videos'):
            os.makedirs('videos')

        # Create directory for each video
        video_dir = f'videos/{title}'
        if not os.path.exists(video_dir):
            os.makedirs(video_dir)

        # Download thumbnail image
        response = requests.get(thumbnail_url)
        if response.status_code == 200:
            # Save thumbnail image to file
            with open(f'{video_dir}/{title}.jpg', 'wb') as f:
                f.write(response.content)

            # Download video
            yt.streams.first().download(f'{video_dir}/')
            print(f'Video "{title}" downloaded successfully.')
        else:
            print(f'Failed to download thumbnail for "{title}".')

    except (AgeRestrictedError, VideoUnavailable) as e:
        print(f'Skipping "{title}" due to: {str(e)}')
