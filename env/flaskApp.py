from flask import Flask, request, jsonify, render_template #Flask create web app, request handles http requests, jsonify converts python dictionary to kson response, render_template to render HTML file
from pytube import YouTube
import re #regular expression
import imageio_ffmpeg as ffmpeg
import os
import librosa
import numpy as np
from pydub import AudioSegment
from moviepy.editor import *
import soundfile as sf

ytURLPattern = r'^(https?://)?(www\.)?youtube\.com/watch\?v=[\w-]+(&\S*)?$' #typical yt url pattern

app = Flask(__name__) #app is webapp

@app.route('/processYTURL', methods=['POST']) #route determines url the webapp is going to respond to and is only going to respond to http POST requests
def process_yt_url():
    try:
        #Get YT URL from request data
        data = request.get_json() #access incoming http request
        ytURL = data['ytURL']
        #validate YTURL
        if not validate_url(ytURL):
            return jsonify({'error': 'Invalid YouTube URL'}), 400
        #Download audio from Youtube
        audioFilePath = download_audio(ytURL)
        if not audioFilePath:
            return jsonify({'error': 'Failed to download audio'}), 500
        #Perform chord recognition
        chordProgression = recognize_chords(audioFilePath)
        if not chordProgression:
            return jsonify({'error':'Chord recognition failed'}), 500
        #Return chord progression to user
        # return render_template('index.html', chordProgression=chordProgression)
        return jsonify({'chordProgression': chordProgression})
    except Exception as e:
        errorMessage = str(e)
        return jsonify({'error': errorMessage}), 500
    
def validate_url(url):
    if re.match(ytURLPattern, url): #check if url matches pattern
        return True
    else:
        return False

def download_audio(url):
    try:
        yt = YouTube(url) #yt object
        #Select stream of downloading
        audio = yt.streams.filter(only_audio=True, file_extension="mp4").first()
        tempAudioFileName = "tempAudioFileName.mp4"
        audio.download(filename=tempAudioFileName) #Download audio to outputPath
        print("Audio downloaded successfully")
        audio_clip = AudioFileClip(tempAudioFileName) #load file
        audio_clip.write_audiofile("output_audio.wav")
        return "output_audio.wav"
    except Exception as e:
        print(f"Error during audio download and conversion: {str(e)}")
        return None

def recognize_chords(audioFilePath):
    try:
        y, sr = librosa.load(audioFilePath) #load file. y is audio signal and se is sample rate
        chroma = librosa.feature.chroma_cqt(y=y, sr=sr) #perform chromagram analysis, pitch class profiles
        chords = librosa.decompose.nn_filter(chroma) #filter by nearest neighbour
        chordProgression = librosa.core.hz_to_note(chords[0]) #convert the indices to chord progression labels
        # return chordLabels
        return ' '.join(chordProgression)
    except Exception as e:
        print(f"Chord recognition error: {str(e)}")
        return None


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)