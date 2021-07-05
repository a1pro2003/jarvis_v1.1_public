from posixpath import expanduser
from random import shuffle
import pandas as pd
from speech_recognition import Microphone, Recognizer, UnknownValueError
import speech_recognition
import spotipy as sp
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os
from os.path import expanduser
from socket import gethostname
from time import sleep
import subprocess
from psutil import process_iter
from sys import exit

"""
To run this script, you must have a file in this directory called 'setup.txt'
In this file, enter all of the values of the required variables in the following format:
client_id=XXXXXXXX
client_secret=XXXXXXX
device_name=Jake's iMac
redirect_uri=https://example.com/callback/
username=jakeg135
scope=user-read-private user-read-playback-state user-modify-playback-state
"""

# Set variables from setup.txt
dir_path = os.path.dirname(os.path.realpath(__file__))
setup = pd.read_csv(dir_path + '/setup.txt', sep='=', index_col=0, squeeze=True, header=None)
client_id = setup['client_id']
client_secret = setup['client_secret']
device_name = setup['device_name']
redirect_uri = setup['redirect_uri']
scope = setup['scope']
username = setup['username']

# Connecting to the Spotify account
auth_manager = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    username=username)
spotify = sp.Spotify(auth_manager=auth_manager)

# Selecting device to play from
devices = spotify.devices()
deviceID = None
for d in devices['devices']:
    d['name'] = d['name'].replace('’', '\'')
    if d['name'] == device_name:
        deviceID = d['id']
        break



class InvalidSearchError(Exception):
    pass


home = expanduser("~")


#checks to see if there is any device avaiable 
#and selectes it if no other device is selected
def auto_select_device():

    device_sel = str(device_selected(spotify=spotify))
    if device_sel == 'False':
        device_act = device_active(spotify=spotify)
        device_id = ''
        if device_act == 'True':
            device = spotify.devices() 
            for d in device['devices']:
                if d['is_active'] == False:
                    device_id = d['id']
                    break
        try:
            spotify.transfer_playback(device_id=device_id, force_play=False)
            sleep(1)
            return 'True'
        except:
            pass
    return device_sel

#Checks if spotify is running
def check_running_program(): #DONE
    return str('Spotify.exe') in (p.name() for p in process_iter())

#Closes spotify if running
def close_spotify(): #DONE
    for proc in process_iter():
        if proc.name() == 'Spotify.exe':
            proc.kill()

#Starts spotify
def start_spotify(): #DONE
    try:
        info = subprocess.STARTUPINFO()
        info.dwFlags = 1
        info.wShowWindow = 0
        if check_running_program() == False:
            spotify_proc = subprocess.Popen(home + '/AppData/Roaming/Spotify/Spotify.exe', startupinfo=info)
    except:
        pass
    return

#checks if there are any devices available
def device_active(spotify: Spotify): #DONE
    device = spotify.devices()
    devices = 0
    for d in device['devices']:
        devices += 1
    if devices == 0:
        return 'False'
    elif devices >= 1:
        return 'True'

#returns device selected
def device_selected(spotify: Spotify): #DONE
    device = spotify.devices()
    
    for d in device['devices']:
        if d['is_active'] == True:
            return 'True'
    return 'False'

#returns device list
def get_device_list(spotify: Spotify): #DONE
    device = spotify.devices()
    device_list = []
    for d in device['devices']:
        device_list.append(d)
    return device_list

#returns current device id
def get_device_id(spotify: Spotify): #DONE
    device = spotify.devices()
    for d in device['devices']:
        if d['is_active'] == True:
            return d['id']

#returns first inactive device id
def get_other_device_id(spotify: Spotify): #DONE
    device = spotify.devices()
    for d in device['devices']:
        if d['is_active'] == False:
            return d['id']

#returns current device name
def get_device_name(spotify: Spotify): #DONE
    device = spotify.devices()
    for d in device['devices']:
        if d['is_active'] == True:
            return d['name']

#returns playing state
def get_playing_state(spotify: Spotify): #DONE
    playing = spotify.current_playback()
    return playing['is_playing']

#returns shuffle state
def get_shuffle_state(spotify: Spotify): #DONE
    playing = spotify.current_playback()
    return playing['shuffle_state']

#returns volume percentage
def get_volume_percent(spotify: Spotify): #DONE
    device = spotify.devices()
    for d in device['devices']:
        if d['is_active'] == True:
            return d['volume_percent']

#returns album uri
def get_album_uri(spotify: Spotify, name: str) -> str:
    """
    :param spotify: Spotify object to make the search from
    :param name: album name
    :return: Spotify uri of the desired album
    """

    # Replace all spaces in name with '+'
    original = name
    name = name.replace(' ', '+')

    results = spotify.search(q=name, limit=1, type='album')
    if not results['albums']['items']:
        raise InvalidSearchError(f'No album named "{original}"')
    album_uri = results['albums']['items'][0]['uri']
    return album_uri

#returns artist uri
def get_artist_uri(spotify: Spotify, name: str) -> str:
    """
    :param spotify: Spotify object to make the search from
    :param name: album name
    :return: Spotify uri of the desired artist
    """

    # Replace all spaces in name with '+'
    original = name
    name = name.replace(' ', '+')

    results = spotify.search(q=name, limit=1, type='artist')
    if not results['artists']['items']:
        raise InvalidSearchError(f'No artist named "{original}"')
    artist_uri = results['artists']['items'][0]['uri']
    print(results['artists']['items'][0]['name'])
    return artist_uri

#returns track uri
def get_track_uri(spotify: Spotify, name: str) -> str:
    """
    :param spotify: Spotify object to make the search from
    :param name: track name
    :return: Spotify uri of the desired track
    """

    # Replace all spaces in name with '+'
    original = name
    name = name.replace(' ', '+')

    results = spotify.search(q=name, limit=1, type='track')
    if not results['tracks']['items']:
        raise InvalidSearchError(f'No track named "{original}"')
    track_uri = results['tracks']['items'][0]['uri']
    return track_uri

#play album
def play_album(spotify=None, device_id=None, uri=None):
    spotify.start_playback(device_id=device_id, context_uri=uri)

#play artist
def play_artist(spotify=None, device_id=None, uri=None):
    spotify.start_playback(device_id=device_id, context_uri=uri)

#play track
def play_track(spotify: None, device_id=None, uri=None):
    spotify.start_playback(device_id=device_id, uris=[uri])

#toggle shuffle state
def toggle_shuffle(spotify: None, device_id=None, state=None): #DONE
    shuffle_state = get_shuffle_state(spotify=spotify)
    if shuffle_state == False and state == 'on':
        spotify.shuffle(True, device_id=get_device_id(spotify=spotify))
        return 'On'

    elif shuffle_state == True and state == 'off':
        spotify.shuffle(False, device_id=get_device_id(spotify=spotify))
        return 'Off'
    else:
        pass

#play users playlist
def play_playlist(spotify: None, device_id: None, playlist: None): #DONE
    results = spotify.current_user_playlists(limit=50)
    playlists = {}
    for i, item in enumerate(results['items']):
        #print("%d %s %s" % (i, item['name'].lower(), item['uri']))
        playlists[str(item['name']).lower()] = item['uri']
    
    for num, name in enumerate(playlists):

        if playlist.lower() in name.lower():
            uri = playlists[name]
            spotify.start_playback(device_id=get_device_id(spotify=spotify), context_uri=uri)




#Handles music request input
def spotify_request(command):

    #checks to see if spotify is running
    if check_running_program() == False:
        start_spotify()
        sleep(2)

    # auto_select_device()
    print("Device selected: " + str(auto_select_device()))


    #check to see if app is running
    if check_running_program() == False:
        start_spotify()


    words = command.split()
    if len(words) <= 0:
        print('Could not understand. Try again')
        return
    #print(words)
    name = ' '.join(words[1:])
    try:
        if words[0] == 'album': #DONE
            try:
                uri = get_album_uri(spotify=spotify, name=name)
                play_album(spotify=spotify, device_id=get_device_id(spotify=spotify), uri=uri)
            except:
                pass

        elif words[0] == 'artist': #DONE
            try:
                uri = get_artist_uri(spotify=spotify, name=name)
                play_artist(spotify=spotify, device_id=get_device_id(spotify=spotify), uri=uri)
            except:
                pass

        elif words[0] == 'play': #DONE
            try:
                uri = get_track_uri(spotify=spotify, name=name)
                play_track(spotify=spotify, device_id=get_device_id(spotify=spotify), uri=uri)
            except:
                pass

        elif ' '.join(words[0:3]) == 'set volume to': #DONE
            try:
                spotify.volume(device_id=get_device_id(spotify=spotify), volume_percent=int(words[3]))
            except:
                pass

        elif ' '.join(words[0:2]) == 'increase volume': #DONE
            try:
                spotify.volume(device_id=get_device_id(spotify=spotify), volume_percent=get_volume_percent(spotify=spotify) + 25)
            except:
                pass

        elif ' '.join(words[0:2]) == 'decrease volume': #DONE
            try:
                spotify.volume(device_id=get_device_id(spotify=spotify), volume_percent=get_volume_percent(spotify=spotify) - 25)
            except:
                pass

        elif words[0] == 'shuffle': #DONE
            try:
                state = None
                try:
                    if words[1]:
                        state = words[1]
                except:
                    pass
                toggle_shuffle(spotify=spotify, state=state)
            except:
                pass

        elif words[0] == 'next': #DONE
            try:
                spotify.next_track(device_id=get_device_id(spotify=spotify))
            except:
                pass

        elif words[0] == 'pause': #DONE
            try:
                if get_playing_state(spotify=spotify) == True:
                    spotify.pause_playback(device_id=get_device_id(spotify=spotify))
            except:
                pass

        elif words[0] == 'resume': #DONE
            try:
                if get_playing_state(spotify=spotify) == False:
                    spotify.start_playback(device_id=get_device_id(spotify=spotify))
                    # sleep(0.1)
                    # spotify.start_playback(device_id=get_device_id(spotify=spotify))
            except:
                pass

        elif ' '.join(words[0:2]) == 'transfer to': #DONE
            try:
                #transfer to TV
                if words[2] == 'tv':
                    spotify.transfer_playback(device_id='7a7ef9e5-46b8-44ca-9309-8e1cfce81fb6')
                
                #trasnfer to computer
                elif words[2] == 'computer':
                    spotify.transfer_playback(device_id='b806a37ebf5690d31761b7e3a3c3f5ad51c9c03c', force_play=True)

                #trasnfer to phone
                elif words[2] == 'phone':
                    spotify.transfer_playback(device_id='b09ac66874e998e1c092a10350e3b54eab0f788b', force_play=True)
            except:
                pass

        elif words[0] == 'playlist':#DONE
            try:
                play_playlist(spotify=spotify, device_id=get_device_id(spotify=spotify), playlist=words[1])
            except:
                pass

        elif words[0] == 'devices': #DONE
            try:
                for d in get_device_list(spotify=spotify):
                    if d['is_active'] == True:
                        print("->:" + d['name'])
                        continue
                    print("  :" + d['name'])
            except:
                pass
            
        elif words[0] == 'exit': #DONE
            close_spotify()
            #exit()

        elif words[0] == 'test':
            device = spotify.devices()
            devices = 0
            for d in device['devices']:
                print(d['name'] + " " + d['id'])


            # try:
            #     for d in get_device_list(spotify=spotify):
            #         if d['is_active'] == True:
            #             print("->:" + d['name'])
            #             continue
            #         print("  :" + d['name'])
            # except:
            #     pass


        else:
            print('Specify either "album", "artist" or "play". Try Again')

    except InvalidSearchError:
        print('InvalidSearchError. Try Again')


# while True: 
#     spotify_request(input("Command: "))