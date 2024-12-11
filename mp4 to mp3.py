import subprocess
import os

def convert_mp4_to_mp3(input_video_path, output_audio_path):
    # Check if the input file exists
    if not os.path.exists(input_video_path):
        raise FileNotFoundError(f"The file {input_video_path} does not exist.")
    
    # Convert MP4 to MP3 using ffmpeg
    subprocess.run(["ffmpeg", "-i", input_video_path, output_audio_path], check=True)
    print(f"Conversion successful! MP3 saved at: {output_audio_path}")


# Define the input and output paths
input_video = r"C:\\Users\\durga\\OneDrive\\Documents\\MP4_to_MP3\\input_video.mp4"  # Input MP4 file path
output_audio = r"C:\\Users\\durga\\OneDrive\\Documents\\MP4_to_MP3\\output_audio.mp3"  # Output MP3 file path

# Call the function with the defined file paths
convert_mp4_to_mp3(input_video, output_audio)