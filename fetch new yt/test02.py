"""
This script downloads thumbnails and videos from YouTube based on video data stored in the "output.json" file. It iterates through each video category and attempts to download the thumbnail image and video for each video.

Workflow:
1. Loads video data from the "output.json" file, which contains YouTube video titles and links organized by category.
2. Iterates through each video category and processes each video within the category.
3. For each video, it extracts the title and link.
4. Attempts to download the thumbnail image using PyTube's thumbnail URL and saves it as "{title}.jpg" in a directory named after the video title within the 'videos' folder.
5. Downloads the video itself using PyTube's first available stream and saves it in the same directory.
6. Prints status messages for successful downloads or skips if the video is age-restricted or unavailable.

Ensure that the "output.json" file contains the expected video data format and that PyTube and requests libraries are installed and accessible to run this script successfully.
"""

import os
import json
from pytube import YouTube
from pytube.exceptions import AgeRestrictedError, VideoUnavailable
import requests

# Load video data from JSON file
with open("output.json", "r") as json_file:
    video_data = json.load(json_file)

# Loop through the list of videos and download each thumbnail
for category in video_data:
    for video in category:
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
