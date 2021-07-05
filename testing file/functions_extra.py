import sys
import speech_recognition as sr
import pyttsx3 as tts
import random
from neuralintents import GenericAssistant
from arrays import *



speaker = tts.init()
speaker.setProperty('rate', 150)
recognizer = sr.Recognizer()

