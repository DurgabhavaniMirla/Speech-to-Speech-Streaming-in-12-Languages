import speech_recognition as sr
from pydub import AudioSegment
from translatepy import Translator

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

# Function to translate text to Hindi
def translate_to_hindi(text):
    translation = translator.translate(text, "Hindi")
    return translation.result

# Main function to handle audio file processing and translation
def translate_audio_file(mp3_path):
    # Convert MP3 to WAV
    wav_path = "converted_audio.wav"
    mp3_to_wav(mp3_path, wav_path)
    
    # Convert audio file (WAV) to text
    english_text = audio_to_text_from_file(wav_path)
    
    if english_text:
        # Translate the recognized English text to Hindi
        hindi_translation = translate_to_hindi(english_text)
        print(f"English: {english_text}")
        print(f"Hindi: {hindi_translation}")
    else:
        print("No text to translate.")

# Path to your MP3 file
mp3_path = "C:\\Users\\durga\\OneDrive\\Documents\\MP4_to_MP3\\output_audio.mp3"

# Run the function to process the MP3 file
translate_audio_file(mp3_path)
