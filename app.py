from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import whisper
import os
import subprocess
from googletrans import Translator
from gtts import gTTS
from pydub import AudioSegment

app = Flask(__name__)

def extract_audio_from_video(input_video_path, output_audio_path):
    if os.path.exists(output_audio_path):
        os.remove(output_audio_path)
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
    if os.path.exists("temp_video.mp4"):
        os.remove("temp_video.mp4")
    subprocess.run(["ffmpeg", "-y", "-i", input_video_path, "-c", "copy", "-an", "temp_video.mp4"], check=True)
    subprocess.run(["ffmpeg", "-y", "-i", "temp_video.mp4", "-i", translated_audio_path, "-c:v", "copy", "-c:a", "aac", output_video_path], check=True)
    os.remove("temp_video.mp4")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate', methods=['POST'])
def translate():
    video_file = request.files['video']
    src_language = request.form['src_language']
    dest_language = request.form['dest_language']

    input_video_path = os.path.join('uploads', video_file.filename)
    video_file.save(input_video_path)

    temp_audio_path = os.path.join('uploads', 'temp_audio.wav')
    translated_audio_path = os.path.join('uploads', 'translated_audio.mp3')
    output_video_path = os.path.join('uploads', 'output_video.mp4')

    extract_audio_from_video(input_video_path, temp_audio_path)
    
    model = whisper.load_model("base")
    result = model.transcribe(temp_audio_path)
    transcribed_text = result['text']
    
    translator = Translator()
    translated = translator.translate(transcribed_text, src=src_language, dest=dest_language)
    translated_text = translated.text
    
    tts = gTTS(translated_text, lang=dest_language)
    tts.save(translated_audio_path)
    
    video_duration = AudioSegment.from_file(input_video_path).duration_seconds * 1000  # in milliseconds
    adjust_audio_duration(translated_audio_path, video_duration)
    
    merge_audio_with_video(input_video_path, translated_audio_path, output_video_path)
    
    os.remove(temp_audio_path)
    os.remove(translated_audio_path)
    os.remove(input_video_path)
    
    return redirect(url_for('display_video', filename='output_video.mp4'))

@app.route('/uploads/<filename>')
def display_video(filename):
    return render_template('display_video.html', filename=filename)

@app.route('/uploads/<filename>')
def send_video(filename):
    return send_from_directory('uploads', filename)

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
