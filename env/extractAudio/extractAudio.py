from pytube import YouTube
import subprocess

ffmpegPath = r"C:\Users\wycmi\Downloads\ffmpeg-master-latest-win64-gpl\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"


def extractAudio(ytURL, outputFile):
    try:
        yt = YouTube(ytURL) #yt object
        #Select stream of downloading
        audio = yt.streams.filter(only_audio=True, file_extension='mp4').first()
        tempAudioFileName = "tempAudioFileName.mp4"
        audio.download(filename=tempAudioFileName) #Download audio to outputPath
        print("Audio downloaded successfully")

        
        #Convert to WAV (higher quality)
        convertCommand = [
            ffmpegPath,
            "-i", tempAudioFileName, #video input file
            "-vn", #no video in output
            "-acodec", "pcm_s16le", #audio codec (PCM 16-bit little-endian)
            "-ar", "44100", #Sets the audio sample rate to 44.1 kHz (standard for audio).
            "-ac", "2", #Sets number of audio channel to 2 for stereo
            outputFile
        ]

        subprocess.run(convertCommand) #Run FFmpeg command
        print("up to here")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False
    
if __name__ == "__main__":
    print("Please enter the Youtube URL:")
    ytURL = str(input())
    if extractAudio(ytURL,"outputAudio.wav"):
        print("heeloo")
    else:
        print("Audio download and conversion failed")