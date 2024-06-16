from flask import Flask, request, render_template, send_file
from pytube import YouTube
from moviepy.editor import AudioFileClip
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

def download_youtube_audio(url):
    try:
        yt = YouTube(url)
        video_title = yt.title
        safe_title = "".join(c if c.isalnum() else "_" for c in video_title)
        output_path = os.path.join(DOWNLOAD_FOLDER, f"{safe_title}.mp3")
        
        audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        
        temp_audio_path = audio_stream.download(filename='temp_audio')
        
        audio_clip = AudioFileClip(temp_audio_path)
        
        audio_clip.write_audiofile(output_path, codec='mp3')
        
        audio_clip.close()
        os.remove(temp_audio_path)
        
        return output_path
    
    except Exception as e:
        return str(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        output_path = download_youtube_audio(url)
        if output_path.endswith('.mp3'):
            return send_file(output_path, as_attachment=True)
        else:
            return f"An error occurred: {output_path}"
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
