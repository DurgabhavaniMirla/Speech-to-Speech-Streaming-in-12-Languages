from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import whisper
import os
import subprocess
from googletrans import Translator
from gtts import gTTS
from pydub import AudioSegment

app = Flask(__name__)

# IMPROVEMENT: Load model once at startup to avoid slow reloads during translation
model = whisper.load_model("base")

# Configuration for uploads
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def extract_audio_from_video(input_video_path, output_audio_path):
    if os.path.exists(output_audio_path):
        os.remove(output_audio_path)
    # Using -y to automatically overwrite existing files
    subprocess.run(["ffmpeg", "-y", "-i", input_video_path, output_audio_path], check=True)

def adjust_audio_duration(audio_path, target_duration):
    audio = AudioSegment.from_file(audio_path)
    if len(audio) > target_duration:
        audio = audio[:target_duration]
    else:
        silence = AudioSegment.silent(duration=(target_duration - len(audio)))
        audio += silence
    audio.export(audio_path, format="mp3")

def merge_audio_with_video(input_video_path, translated_audio_path, output_video_path):
    temp_no_audio = "temp_no_audio.mp4"
    if os.path.exists(temp_no_audio):
        os.remove(temp_no_audio)
    
    # Remove audio from original video
    subprocess.run(["ffmpeg", "-y", "-i", input_video_path, "-c", "copy", "-an", temp_no_audio], check=True)
    # Merge new translated audio with the video
    subprocess.run(["ffmpeg", "-y", "-i", temp_no_audio, "-i", translated_audio_path, "-c:v", "copy", "-c:a", "aac", output_video_path], check=True)
    
    if os.path.exists(temp_no_audio):
        os.remove(temp_no_audio)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    video_file = request.files['video']
    # FIX: Removed src_language request to match your updated UI
    dest_language = request.form['dest_language']

    input_video_path = os.path.join(UPLOAD_FOLDER, video_file.filename)
    video_file.save(input_video_path)

    temp_audio_path = os.path.join(UPLOAD_FOLDER, 'temp_audio.wav')
    translated_audio_path = os.path.join(UPLOAD_FOLDER, 'translated_audio.mp3')
    
    # Unique output filename to avoid caching issues
    output_filename = 'translated_' + video_file.filename
    output_video_path = os.path.join(UPLOAD_FOLDER, output_filename)

    # 1. Pipeline: Extraction
    extract_audio_from_video(input_video_path, temp_audio_path)
    
    # 2. Pipeline: AI Transcription (Whisper handles language detection automatically)
    result = model.transcribe(temp_audio_path)
    transcribed_text = result['text']
    
    # 3. Pipeline: Neural Translation
    translator = Translator()
    # Whisper detected the source, so we only need to provide the destination
    translated = translator.translate(transcribed_text, dest=dest_language)
    translated_text = translated.text
    
    # 4. Pipeline: Speech Synthesis
    tts = gTTS(translated_text, lang=dest_language)
    tts.save(translated_audio_path)
    
    # 5. Pipeline: Audio Synchronization
    video_info = AudioSegment.from_file(input_video_path)
    video_duration = len(video_info)  # Duration in milliseconds
    adjust_audio_duration(translated_audio_path, video_duration)
    
    # 6. Pipeline: Merging
    merge_audio_with_video(input_video_path, translated_audio_path, output_video_path)
    
    # Cleanup to save storage
    if os.path.exists(temp_audio_path): os.remove(temp_audio_path)
    if os.path.exists(translated_audio_path): os.remove(translated_audio_path)
    if os.path.exists(input_video_path): os.remove(input_video_path)
    
    return redirect(url_for('display_video', filename=output_filename))

@app.route('/display/<filename>')
def display_video(filename):
    return render_template('display_video.html', filename=filename)

@app.route('/uploads/<filename>')
def send_video(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
