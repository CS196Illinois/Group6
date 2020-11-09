# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 22:39:27 2020

@author: jmalc
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