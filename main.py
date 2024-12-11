import speech_recognition as sr
from pydub import AudioSegment
from translatepy import Translator
from gtts import gTTS
from moviepy import VideoFileClip, AudioFileClip
import os

# Initialize the recognizer and translator
recognizer = sr.Recognizer()
translator = Translator()

# Function to extract audio from video and save it as a WAV file
def extract_audio_from_video(video_path, audio_path):
    try:
        video = VideoFileClip(video_path)
        audio = video.audio
        audio.write_audiofile(audio_path)
        print(f"Audio extracted from video: {audio_path}")
    except Exception as e:
        print(f"Error extracting audio from video: {e}")

# Function to convert MP3 to WAV
def mp3_to_wav(mp3_path, wav_path):
    try:
        audio = AudioSegment.from_mp3(mp3_path)
        audio.export(wav_path, format="wav")
        print(f"Converted MP3 to WAV: {wav_path}")
    except Exception as e:
        print(f"Error converting MP3 to WAV: {e}")

# Function to convert audio (WAV) to text
def audio_to_text_from_file(wav_path):
    with sr.AudioFile(wav_path) as source:
        print("Converting audio to text...")
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            print(f"Recognized text: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            return None
        except sr.RequestError:
            print("Sorry, the speech recognition service is unavailable.")
            return None

# Function to translate text from English to Telugu
def translate_to_telugu(text):
    translation = translator.translate(text, "Telugu")
    return translation.result

# Function to convert text to speech in Telugu
def text_to_speech_telugu(text, output_audio):
    try:
        tts = gTTS(text=text, lang='te', slow=False)  # 'te' is the language code for Telugu
        tts.save(output_audio)
        print(f"Speech saved to {output_audio}")
        
        # Play the saved audio file (optional, if you want to play it immediately)
        os.system(f"start {output_audio}")  # Works on Windows, for Mac use 'open', Linux use 'xdg-open'
    except Exception as e:
        print(f"Error converting text to speech: {e}")

# Function to combine audio with video
def combine_audio_with_video(video_file, audio_file, output_file):
    video = VideoFileClip(video_file)
    audio = AudioFileClip(audio_file)
    video_with_new_audio = video.with_audio(audio)  # Use with_audio instead of set_audio
    video_with_new_audio.write_videofile(output_file, codec="libx264")

# Main function to process video, translate speech, and combine translated speech back into video
def process_video_and_translate(video_path):
    # Step 1: Extract audio from video
    extracted_audio_path = "extracted_audio.mp3"
    extract_audio_from_video(video_path, extracted_audio_path)
    
    # Step 2: Convert MP3 audio to WAV
    wav_path = "converted_audio.wav"
    mp3_to_wav(extracted_audio_path, wav_path)
    
    # Step 3: Convert audio (WAV) to text (English)
    english_text = audio_to_text_from_file(wav_path)
    
    if english_text:
        # Step 4: Translate English text to Telugu
        telugu_translation = translate_to_telugu(english_text)
        print(f"English Text: {english_text}")
        print(f"Translated Telugu Text: {telugu_translation}")
        
        # Step 5: Convert the translated Telugu text to speech
        translated_audio_path = "translated_audio.mp3"
        text_to_speech_telugu(telugu_translation, translated_audio_path)
        
        # Step 6: Combine translated audio with the original video
        output_video_file = "output_video_with_translated_audio.mp4"
        combine_audio_with_video(video_path, translated_audio_path, output_video_file)
        print(f"Output video saved as {output_video_file}")
    else:
        print("No text to translate.")

# Path to your input video
video_path = "C:\\Users\\durga\\OneDrive\\Documents\\MP4_to_MP3\\input_video.mp4"

# Run the function to process the video
process_video_and_translate(video_path)
