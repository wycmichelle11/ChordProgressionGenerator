import librosa
#import librosa.display



def recognizeChords(audioFile):
    y, sr = librosa.load(audioFile) #load audio file
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr) #perform chromagram analysis, pitch class profiles
    chords = librosa.decompose.nn_filter(chroma) #filter by nearest neighbour
    chordLabels = librosa.core.hz_to_note(chords[0]) #convert the indices to chord progression labels
    return chordLabels

if __name__ == "__main__":
    audioFile=r"../extractAudio/outputAudio.wav"
    chordProgression = recognizeChords(audioFile)
    print(chordProgression)