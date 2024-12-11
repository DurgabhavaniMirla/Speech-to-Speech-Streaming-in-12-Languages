import speech_recognition as sr
from pydub import AudioSegment
from translatepy import Translator
from gtts import gTTS
import os

# Initialize the recognizer and translator
recognizer = sr.Recognizer()
translator = Translator()

# Function to convert MP3 to WAV
def mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")
    print(f"Converted MP3 to WAV: {wav_path}")

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
def text_to_speech_telugu(text):
    tts = gTTS(text=text, lang='te', slow=False)  # 'te' is the language code for Telugu
    output_path = "output_telugu_speech.mp3"
    tts.save(output_path)
    print(f"Speech saved to {output_path}")
    
    # Play the saved audio file (optional, if you want to play it immediately)
    os.system(f"start {output_path}")  # Works on Windows, for Mac use 'open', Linux use 'xdg-open'

# Main function to process audio file, translate, and convert to Telugu speech
def process_audio_and_translate(mp3_path):
    # Step 1: Convert MP3 to WAV
    wav_path = "converted_audio.wav"
    mp3_to_wav(mp3_path, wav_path)
    
    # Step 2: Convert audio file (WAV) to text (English)
    english_text = audio_to_text_from_file(wav_path)
    
    if english_text:
        # Step 3: Translate English text to Telugu
        telugu_translation = translate_to_telugu(english_text)
        print(f"English Text: {english_text}")
        print(f"Translated Telugu Text: {telugu_translation}")
        
        # Step 4: Convert the translated Telugu text to speech
        text_to_speech_telugu(telugu_translation)
    else:
        print("No text to translate.")

# Path to your MP3 file
mp3_path = "C:\\Users\\durga\\OneDrive\\Documents\\MP4_to_MP3\\output_audio.mp3"

# Run the function to process the audio file
process_audio_and_translate(mp3_path)
