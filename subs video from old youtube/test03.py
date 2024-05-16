"""
This script automates the process of managing YouTube video data for users based on their viewing history:

1. Retrieval: It extracts video details like title, author, description, views, length, rating, upload date, and thumbnail URL from YouTube links stored in the "output.json" file.

2. Filtering: Videos are filtered based on a user-defined threshold date, indicating the last date they viewed the channel. Videos uploaded after this date are considered new and relevant.

3. Updating: Filtered videos are then overwritten back to "output1.json", ensuring users have an updated list of videos they haven't viewed yet.

Ensure the "output.json" file contains YouTube video links in the expected format, and set the threshold date to the last date you viewed the channel to filter out newer videos.
"""

import json
from pytube import YouTube
from datetime import datetime, timedelta
from pytube.exceptions import VideoPrivate

def get_video_info(url):
    try:
        # Create a YouTube object
        yt = YouTube(url)
        
        # Extract video details
        title = yt.title
        author = yt.author
        description = yt.description
        views = yt.views
        length = yt.length
        rating = yt.rating
        upload_date = yt.publish_date
        thumbnail_url = yt.thumbnail_url

        upload_date += timedelta(days=1)
        
        # Return video details
        return {
            "title": title,
            "author": author,
            "description": description,
            "views": views,
            "length": length,
            "rating": rating,
            "upload_date": upload_date,
            "thumbnail_url": thumbnail_url
        }
    except VideoPrivate:
        return None  # Skip processing private videos

video_data = []

# Read video data from the "output.json" file
with open("output.json", "r") as json_file:
    video_data = json.load(json_file)

# Define the threshold date (20 May 2024)
threshold_date = datetime(2024, 5, 20)

# Filter videos based on upload date
filtered_videos = []

for category in video_data:
    for video in category:
        video_info = get_video_info(video['link'])
        if video_info and video_info["upload_date"] > threshold_date:
            print(video['title'])
            filtered_videos.append(video)

# Overwrite the "output.json" file with the filtered videos
with open("output1.json", "w") as json_file:
    json.dump(filtered_videos, json_file, indent=2)

print("Filtered videos have been written back to the output.json file.")
