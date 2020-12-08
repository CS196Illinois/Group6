
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 22:39:27 2020

@author: jmalc
inputs: 
    file - audio file to be transcribed
    length - the number of seconds of the audio file to be transcribed
    start - the starting second of recording
params:
    speech - the audiofile
    recog - an instance of a Recognizer() created for recognition functionality
    audio - uses the .record method to record the audio file for use
prints:
    .recognize_google() - takes the recording and uses the Google Speech 
        Recognition API to transcribe into text (can use other APIs)
    "unclear audio" - if .recognize_google() fails, tell the user
"""
import speech_recognition as sr

recog = sr.Recognizer()
file = input('Enter an audio file: ')
length = input('How much of the file would you like to use? (for all, type "all")')
if length == "all":
    speech = sr.AudioFile(file)
    with speech as filesource:
        recog.adjust_for_ambient_noise(filesource)
        audio = recog.record(filesource)
        try:
            recog.recognize_google(audio)
            print(recog.recognize_google(audio))
        except:
            print("unclear audio")
else:
    start = int(input('Where would you like the recording to start?'))
    length = int(length)
    speech = sr.AudioFile(file)
    with speech as filesource:
        recog.adjust_for_ambient_noise(filesource)
        audio = recog.record(filesource, offset=start, duration=length)
        try:
            recog.recognize_google(audio)
            print(recog.recognize_google(audio))
        except:
            print("unclear audio")