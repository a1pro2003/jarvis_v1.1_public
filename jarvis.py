from email import message
import sys
from urllib import request
from warnings import resetwarnings
import speech_recognition as sr
import pyttsx3 as tts
import random
from neuralintents import GenericAssistant
import pyjokes
import json
import time
import csv


from modules.files.arrays import *
from modules.files.json_data import *
from modules.spotify.spotify import *
from modules.tv_control.lg import *
from modules.tv_control.connection import *
from modules.tv_control.controls import *
from modules.tv_control.discovery import *
from modules.tv_control.model import *
from modules.emails.send_emails import *
# from modules.tv_control.scanner import *
from modules.tv_control.network import *


speaker = tts.init()
# speaker.setProperty('rate', 130)
en_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\MSTTS_V110_enGB_GeorgeM"
speaker.setProperty('voice', en_voice_id) # sets voice
recognizer = sr.Recognizer()

current_dir_path = str(os.path.dirname(os.path.realpath(__file__)))
user_dir_path = str(Path.home())
home = expanduser("~")
modules_dir = '/modules'
modules_files_dir = '/modules/files'



###############################################################
#
#
#           Core Functions
#
#
###############################################################

def get_audio(): #DONE

    try:
        with sr.Microphone() as mic:
            recognizer = sr.Recognizer()
            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            input_audio = recognizer.listen(mic)
            audio = ''
            audio = recognizer.recognize_google(input_audio)
            audio = audio.lower()
        #assistant.request(audio)
    except sr.UnknownValueError:
        recognizer = sr.Recognizer()

def listen(): #DONE
    global audio
    DONE = False
    audio = ''
    while not DONE:
        try:
            with sr.Microphone() as mic:
                # recognizer = sr.Recognizer()
                # recognizer.adjust_for_ambient_noise(mic, duration=0.5)
                # recognizer.energy_threshold = 3500
                # input_audio = recognizer.listen(mic)
                # audio = ''
                # audio = recognizer.recognize_google(input_audio)

                r = sr.Recognizer()
                r.adjust_for_ambient_noise(mic, duration=1)
                r.dynamic_energy_threshold = True
                r.energy_threshold = 3600 # between 4400 to 4600
                r.pause_threshold = 1.2
                record = r.record(mic, duration = 6) #works nice   
                #record = r.listen(mic)             
                audio = r.recognize_google(record).lower()

                DONE = True
                return audio.lower()
        except sr.UnknownValueError:
            pass
    
def listen_1():
    try:
        with sr.Microphone() as mic:
            r = sr.Recognizer()
            r.adjust_for_ambient_noise(mic, duration=1)
            r.dynamic_energy_threshold = True
            r.energy_threshold = 3600 # between 4400 to 4600
            r.pause_threshold = 1.2
            #record = r.record(mic, duration = 5) #works nice   
            record = r.listen(mic)             
            audio = r.recognize_google(record).lower()

            DONE = True
            return audio.lower()
    except sr.UnknownValueError:
        pass

def speak(audio): #DONE
    speaker.say(audio)
    speaker.runAndWait()

def cleanup():
    #KIlls spotify if running
    speak(goodbye_responses[random.randint(0, len(goodbye_responses) - 1)])
    close_spotify()
    tv_controls('notification power off')
    sys.exit()

###############################################################
#
#
#           Extra Functions
#
#
###############################################################


def greeting_res(): #DONE
    message = greeting_responses[random.randint(0, len(greeting_responses)-1)]
    print("Alexa: " + message)
    speak(message)

def create_note_res():
    #create notes in a folder and file
    global recognizer
    speaker.say("What do you want to add to your note?")
    print("Alexa: " + "What do you want to add to your note?")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            with sr.Microphone() as mic:
                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                speaker.say("choose a file name")
                print("Alexa: choose a filename")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower()
                print("Me: " + str(filename))

            with open(f"{filename}.txt", 'w') as f:
                f.write(note)
                done = True
                speaker.say("Successfully made {}".format(filename))
                print("Alexa: " + "Successfully made {}".format(filename))
                speaker.runAndWait()

        except sr.UnknownValueError:
            recognizer = sr.Recognizer()
            speaker.say("I did not understand")
            print("Alexa: I did not understant")
            speaker.runAndWait()

def show_todo_res(): #Done
    #Make todo list in a folder and file to be able to access it even after shutdown
    global todo_list
    speaker.say("Showing to do list ")
    print("Alexa: Showing to-do list")

    #iterates throu to-do list and prints the tasks
    for task_num, task_val in task_list().items():
        print(task_num + ": " + task_val)
        speaker.say(task_num + ": " + task_val)


    speaker.runAndWait()

def add_todo_res(): #Done
    speaker.say("What do u want to add")
    print("Alexa: What do you want to add")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            #listens for item to be added to tasks
            item = listen()

            #checks to see cancel
            if 'cancel' in item or 'never mind' in item:
                cancel_res()
                break

            #adds task
            task_add(item)

            done = True

            speaker.say("Item {} added".format(item))
            print("Alexa: " +  "Item {} added".format(item))
            speaker.runAndWait()

                
        except:
            recognizer = sr.Recognizer()
            speaker.say("I did not understand")
            print("Alexa: I did not understant")
            speaker.runAndWait()

def remove_todo_res(): #Done
    speaker.say("What task do you want to remove")
    print("Alexa: " + "What task do you want to remove")
    speaker.runAndWait()

    done = False

    while not done:
        try:
            #listens for number and sanitises the input to be left with an int
            item = listen().replace('task', '')

            if 'cancel' in item or 'never mind' in item:
                cancel_res()
                break
            
            item = item.replace('number', '')
            item = item.replace(' ', '')

            #ensures the first few numbers are assigned to an int
            if item == 'one':
                item = 1
            elif item == 'two':
                item = 2
            elif item == 'three':
                item = 3
            elif item == 'for':
                item = 4

            #deletes a task with given task number
            task = task_delete(int(item))
            
            #checks to see if the item was deleted or in list
            if task == False:
                speak("Item not in list")
                break
            
            done = True

            speaker.say("Item {} removed".format(item))
            print("Alexa: " + "Item {} removed".format(item))
            speaker.runAndWait()

                
        except:
            recognizer = sr.Recognizer()
            speaker.say("I did not understand")
            print("Alexa: I did not understant")
            speaker.runAndWait()

def thank_you_res(): #DONE
    response = thank_you_responses[random.randint(0,len(thank_you_responses) - 1)]
    print("Alexa: " + response)
    return speak(response)

def cancel_res(): #DONE
    response = cancel_responses[random.randint(0,len(cancel_responses)-1)]
    print("Alexa: " + response)
    return speak(response)

def joke_res(): #DONE
    joke = pyjokes.get_joke()
    speak(joke)
    print("Alexa: " + joke)

def music_request_res(request):
    #Check if spotify is running, if not, exedcute it
    spotify_request(request)

def tv_request_res(request):
    #Check if spotify is running, if not, exedcute it
    tv_controls(request)
    
def send_email_res():
    DONE = False
    while not DONE:
        try:
            speak('Who do you want to send the email to')
            print("Alexa: " + "Who do you want to send the email to")
            to = listen()
            print("Me: " + to)
            with open(current_dir_path + modules_dir + '/emails/email_dict.csv', 'r') as f:
                csv_reader = csv.reader(f, delimiter=',')
                pass_count = 0
                for row in csv_reader:
                    if pass_count == 0:
                        pass_count += 1
                        continue
                    if row[0] == to:
                        to = row[1]
                        break
        except:
            speak('Could not catch that, repeat')
            print("Alexa: " + "Could not catch that, repeat")
            continue

        try:
            speak('Subject of email')
            print("Alexa: " + "Subject of email")
            subject = listen()
            print("Me: " + subject)
        except:
            speak('Could not catch that, repeat')
            print("Alexa: " + "Could not catch that, repeat")
            continue

        try:
            speak('Meesage')
            print("Alexa: " + "Message")
            body = listen()
            print("Me: " + body)
        except:
            speak('Could not catch that, repeat')
            print("Alexa: " + "Could not catch that, repeat")
            continue
        result = email_msg(subject=subject, body=body, to=to)
        if result == True:
            speak('Message sent successfully')
            print("Alexa: " + "Message sent successfully")
        elif result == False:
            speak('Message not delivered')
            print("Alexa: " + "Message not delivered")
        DONE = True

    

#Music Playing Function

#

###############################################################
#
#
#           Loop
#
#
###############################################################





def main():
    while True:
        global assistant
        WAKE = 'alexa'
        MUSIC = 'music'
        TV = 'tv'
        try:
            with sr.Microphone() as mic:
                input = listen()

            input.lower()
            #checks to see if music
            if (input.count(MUSIC) > 0):
                print("Me: " + input)
                music_request_res(input.replace('music', ''))
                continue

            elif (input.count(TV) > 0):
                print("Me: " + input)
                tv_request_res(input.replace('tv', ''))
                continue

            #checks to see if 'Alexa' is in sentence
            elif (input.count(WAKE) > 0) or (WAKE in input):
                print('Alexa: yh?')
                input = input.replace('alexa ', '')
                input = input.replace('alexa', '')
                print("Me:" + input)
                input_list = input.split()
                print(input_list)



                if len(input_list) <= 0:
                    continue 


                else:
                    assistant.request(input)
                    pass
                continue
            


        except sr.UnknownValueError:
            pass


mappings = {
    "greeting": greeting_res,
    "create_note": create_note_res,
    "add_todo": add_todo_res,
    "show_todo": show_todo_res,
    "remove_todo": remove_todo_res,
    "cancel": cancel_res,
    "thank_you": thank_you_res,
    "joke": joke_res,
    "bye": cleanup,
    "send_email": send_email_res,
}
# print(current_dir_path + modules_files_dir + '/intents.json')
assistant = GenericAssistant(current_dir_path + modules_files_dir + '/intents.json', intent_methods=mappings)

# #Checks to see if 'intents.json' has changed to determine wether to re-train the AI
# #DONE
# if intents_size() == get_intents_size():
#     assistant.load_model()
# elif intents_size() != get_intents_size():
#     assistant.train_model()
#     assistant.save_model()
#     write_intents_size()

assistant.train_model()


speak("Hello")
print("Hello")
main()
