import speech_recognition as sr
import moviepy.editor


#Converts video file to audio
video = moviepy.editor.VideoFileClip('talking.mp4');
audio = video.audio;
audio.write_audiofile('SOUND_talking.wav')

#Converts audio file to text
def main():
    sound = "SOUND_talking.wav"

    r = sr.Recognizer()


    with sr.AudioFile(sound) as source:
        r.adjust_for_ambient_noise(source)
        print("Converting Audio To Text ..... ")
        audio = r.listen(source)

    try:
        print("Converted Audio Is : \n" + r.recognize_google(audio))

    except Exception as e:
        print("Error {} : ".format(e) )



if __name__ == "__main__":
    main()