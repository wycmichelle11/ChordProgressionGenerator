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
        print("made it here")
        print(ytURL)
        #validate YTURL
        if not validate_url(ytURL):
            return jsonify({'error': 'Invalid YouTube URL'}), 400
        print("made it here2")
        #Download audio from Youtube
        audioFilePath = download_audio(ytURL)
        if not audioFilePath:
            return jsonify({'error': 'Failed to download audio'}), 500
        print("made it here3")
        #Perform chord recognition
        chordProgression = recognize_chords(audioFilePath)
        if not chordProgression:
            return jsonify({'error':'Chord recognition failed'}), 500
        print("made it here4")
        #Return chord progression to user
        return render_template('index.html', chordProgression=chordProgression)
    
    except Exception as e:
        errorMessage = str(e)
        return jsonify({'error': errorMessage}), 500
    
def validate_url(url):
    print("did it validate?")
    if re.match(ytURLPattern, url): #check if url matches pattern
        print("it is valid")
        return True
    else:
        print("it is invalid")
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
        print("wadeee")
        audio_clip.write_audiofile("output_audio.wav")
        print("here")
        return "output_file.wav"
    except Exception as e:
        print(f"Error during audio download and conversion: {str(e)}")
        return None

def recognize_chords(audioFilePath):
    try:
        y, sr = librosa.load(audioFilePath) #load file. y is audio signal and se is sample rate
        yHarmonic, yPercussive = librosa.effects.hpss(y) #decompose harmonic and percussive parts
        chromagram = librosa.feature.chroma_cens(y=yHarmonic, sr=sr) #extract chroma (pitch components)
        chromagram = np.transpose(chromagram) #transpose for better recognition
        chords = librosa.segment.recurrence_matrix(chromagram)
        chordLabels = librosa.decompose.nn_filter(chords, aggregate=np.median) #filter by nearest neighbour feature
        chordSymbols = librosa.hz_to_midi(chordLabels)
        chordProgression = [librosa.midi_to_note(chord) for chord in chordSymbols] #convert to readable chordnames
        return ' '.join(chordProgression)
    except Exception as e:
        print(f"Chord recognition error: {str(e)}")
        return None


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)