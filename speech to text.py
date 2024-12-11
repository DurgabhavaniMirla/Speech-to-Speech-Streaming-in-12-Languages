from transformers import pipeline
import torch

# Load the whisper model pipeline
speech_to_text = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-large-v3",
    device=0 if torch.cuda.is_available() else -1
)

# Function to process audio file
def transcribe_audio(file_path):
    # Perform speech-to-text conversion
    result = speech_to_text(file_path)
    return result['text']

# Example: Providing a file path
if __name__ == "__main__":
    # Replace 'path_to_audio_file' with the actual file path
    file_path = "C:\\Users\\durga\\OneDrive\\Documents\\MP4_to_MP3\\output_audio.mp3"
    transcription = transcribe_audio(file_path)
    print("\nTranscription:")
    print(transcription)
