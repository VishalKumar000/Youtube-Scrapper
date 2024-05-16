import os
import subprocess

# Function to clip a video to 55 seconds
def clip_video(file):
    try:
        filename = os.path.basename(file)
        duration = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file]))
        if duration > 55:
            output_file = f"clipped_{filename}"
            command = ['ffmpeg', '-i', file, '-ss', '0', '-t', '55', '-c:v', 'copy', '-c:a', 'copy', output_file, '-y']
            subprocess.run(command, capture_output=True)
            print(f"Clipped {filename} to 55 seconds. Saved as {output_file}")
            os.remove(file)
            os.rename(output_file, file)  # Replace original with clipped version
        # else:
        #     print(f"{filename} is already less than or equal to 55 seconds")
    except Exception as e:
        print(f"Error processing {file}: {e}")

# Function to recursively search for video files in a directory
def get_video_files(directory):
    video_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith((".mp4", ".webm", ".mkv")):
                video_files.append(os.path.join(root, file))
    return video_files

# Get the current directory
current_dir = os.getcwd()

# Get a list of all video files in the current directory and its subdirectories
video_files = get_video_files(current_dir)

# Clip videos longer than 55 seconds
for video_file in video_files:
    clip_video(video_file)
