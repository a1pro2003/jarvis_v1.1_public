from logging import info
from random import randint, shuffle
from numpy.lib.nanfunctions import nanmean
import pandas as pd
from speech_recognition import Microphone, Recognizer, UnknownValueError
import speech_recognition
import spotipy as sp
from spotipy import Spotify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
import subprocess
import psutil
from os.path import expanduser
from time import sleep
from subprocess import check_output
import signal

home = expanduser("~")

def check_running_program(program):
    return str(program) in (p.name() for p in psutil.process_iter())

def start_spotify():
    info = subprocess.STARTUPINFO()
    info.dwFlags = 1
    info.wShowWindow = 0
    #subprocess.run([home + '\\AppData\\Roaming\\Spotify\\Spotify.exe'])
    #subprocess.call(home + '\\AppData\\Roaming\\Spotify\\Spotify.exe') #for windows #C:\Users\Adrian\AppData\Roaming\Spotify
    if check_running_program('Spotify.exe') == False:
        spotify_proc = subprocess.Popen(home + '\\AppData\\Roaming\\Spotify\\Spotify.exe', startupinfo=info)
    return

def close_spotify():
    for proc in psutil.process_iter():
        if proc.name() == 'Spotify.exe':
            #print(proc.name())
            proc.kill()

def get_pid(name):
    return check_output(["pidof",name])

if check_running_program('Spotify.exe') == False:
    start_spotify()
    sleep(8)


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
    print(d)
    d['name'] = d['name'].replace('’', '\'')
    #Selects computer
    if d['name'] == device_name:
        deviceID = d['id']
        break
    
    # #Selects computer
    # if d['type'] == 'Computer':
    #     deviceID = d['id']
    #     break



########
#
#
#   Core Functions
#
#
########



class InvalidSearchError(Exception):
    pass

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


def get_shuffle_state():
    try:
        information = spotify.current_playback()
        return information['shuffle_state']
    except:
        return


def get_playing_state():
    try:
        information = spotify.current_playback()
        playing = information['is_playing']
    except:
        return
    return playing


def get_volume_percent():
    device = spotify.devices()
    for d in device['devices']:
        if d['volume_percent'] == 'True':
            return d['name']


def get_device_id():
    device = spotify.devices()
    for d in device['devices']:
        if d['is_active'] == True:
            return d['id']

def get_other_device_id():
    device = spotify.devices()
    print(device)
    print("\n")
    for d in device['devices']:
        if d['is_active'] == False:
            print(d['id'])
            return d['id']


def get_device_name():
    device = spotify.devices()
    #print(device['devices'][0]['name'])
    for d in device['devices']:
        if d['is_active'] == True:
            return d['name']





# information = spotify.current_playback()
# device_id = information['device']['id']
# volume = information['device']['volume_percent']
# shuffle_state = information['shuffle_state']
# playing_state = information['is_playing']

########
#
#
#   Functions
#
#
########



def spotify_request(command):

    request = command.split()
    # if len(request) <= 1:
    #     print('Could not understand. Try again')
    #     return
    name = ' '.join(request[1:])

    device = spotify.devices()
    count = len(device['devices'])
    max = 0
    for d in device['devices']:
        max += 1
        if d['is_active'] == True:
            print("active: " + d['name'])
        elif max == count:
            print("incactive: " + d['name'])


        
            

    try:


        #commands for computer
        if get_device_name() == 'ADRIAN-PC':

            if request[0] == 'resume':
                if get_playing_state() == False:
                    resume_playback(device_id=get_device_id())
            
            elif request[0] == 'pause':
                if get_playing_state() == True:
                    pause_playback(device_id=get_device_id())

            elif ' '.join(request[0:3]) == 'set volume to':
                set_volume(volume=int(request[3]), device_id=get_device_id())

            elif request[0] == 'next':
                next_track(device_id=get_device_id())

            elif request[0] == 'shuffle':
                state = tog_shuffle(get_shuffle_state, device_id=get_device_id())
                #print("Shuffle toggled: " + str(state))
            
            elif ' '.join(request[0:2]) == 'transfer to':
                transfer_playback(device_name=request[2], device_id=str(get_other_device_id()))

            elif request[0] == 'album':
                uri = get_album_uri(spotify=spotify, name=name)
                play_album(spotify=spotify, device_id=get_device_id(), uri=uri)

            elif request[0] == 'artist':
                uri = get_artist_uri(spotify=spotify, name=name)
                play_artist(device_id=get_device_id(), uri=uri)

            elif request[0] == 'play':
                uri = get_track_uri(spotify=spotify, name=name)
                play_track(spotify=spotify, device_id=get_device_id(), uri=uri)

            elif request[0:2] == 'set volume to':
                spotify.volume(client_id=get_device_id(), volume_percent=int(request[3]))
            
            elif request[0:1] == 'increase volume':
                spotify.volume(device_id=get_device_id(), volume_percent=int(get_volume_percent()) + 25)

            elif request[0:1] == 'decrease volume':
                spotify.volume(device_id=get_device_id, volume_percent=int(get_volume_percent()) - 25)

            elif request[0] == 'playlist':
                play_playlist(str(request[1]), client_id=get_device_id())

            elif request[0] == 'test':

                name = str(request[1:])
                name = name.replace(' ', '+')
                #search song
                # uris = spotify.search(name, limit=3, type='track')
                
                # uri_name = []
                # uri_list = []

                # count = 0
                # for uri in uris['tracks']['items']:
                #     uri_list.append(uri['uri'])
                #     uri_name.append(uri['name'])
                #     count += 1

                # print(uri_list)
                # print(uri_name)
                # spotify.start_playback(device_id = 'b806a37ebf5690d31761b7e3a3c3f5ad51c9c03c', uris=uri_list)
                
                #make random list from liked playlist of 100 songs
                amount = 10
                number = randint(0, 1000)
                liked_playlist = []
                for trackk in range(amount):
                    liked_tracks = spotify.current_user_saved_tracks(limit = 1, offset = number)
                    track = liked_tracks['items'][0]['track']
                    #print("random int: " + str(number))
                    #print("%32.32s %s" % (track['artists'][0]['name'], track['name']))
                    #print("%32.32s %s" % (track['artists'][0]['uri'], track['name']))
                    liked_playlist.append(track['uri'])
                    number = randint(0, 1000)
                print(liked_playlist)

                #list all the users playlist
                results = spotify.current_user_playlists(limit=50)
                playlists = {}
                for i, item in enumerate(results['items']):
                    print("%d %s" % (i, item['name']))
                    print("%d %s" % (i, item['uri']))
                    playlists[item['name']] = item['uri']


                information = spotify.current_playback()
                playing = information['is_playing']
                print(playing)

            
            else:
                print('Specify either "album", "artist" or "play". Try Again')



        #commands for phone        
        else:
            if ' '.join(request[0:2]) == 'transfer to':
                transfer_playback(device_name=request[2], device_id=str(get_other_device_id()))


    except InvalidSearchError:
        print('InvalidSearchError. Try Again')
  

def resume_playback(device_id):
    spotify.start_playback(device_id = device_id)

def pause_playback(device_id):
    spotify.pause_playback(device_id = device_id)

def set_volume(volume, device_id):
    spotify.volume(volume, device_id)

def next_track(device_id):
    spotify.next_track(device_id = device_id)

def tog_shuffle(shuffle_state,device_id):
    if shuffle_state == True:
        spotify.shuffle(False, device_id = device_id)
        return 'Off'
    elif shuffle_state == False:
        spotify.shuffle(True, device_id = device_id)
        return 'On'

def transfer_playback(device_name=None, device_id=None):
    if device_name == 'phone':
        
        try:
            spotify.transfer_playback(device_id=device_id, force_play=True)
        except:
            print("error?!!")
    elif device_name == 'computer':
        try:
            spotify.transfer_playback(device_id=device_id, force_play=True)
        except:
            print("error?!!")
    else:
        return 'Device not avaiable'

def play_album(spotify=None, uri=None, device_id=None):
    spotify.start_playback(device_id = device_id, context_uri=uri)

def play_artist(spotify=None, uri=None, device_id=None):
    spotify.start_playback(device_id = device_id, context_uri=uri)

def play_track(spotify=None, uri=None, device_id=None):
    spotify.start_playback(device_id = get_device_id(), uris=[uri])

def play_playlist(playlist, device_id):
    print(playlist)
    results = spotify.current_user_playlists(limit=50)
    playlists = {}
    for i, item in enumerate(results['items']):
        print("%d %s" % (i, item['name']))
        print("%d %s" % (i, item['uri']))
        playlists[str(item['name']).lower()] = item['uri']
        print(str(item['name']).lower())
    
    print('\n')
    for name, uri in enumerate(playlists):

        print(name)
        print(uri)
        if playlist in str(uri):
            uri = playlists[uri]
            spotify.start_playback(device_id = device_id, context_uri=uri)

# play_track(device_id=get_device_id(), uri=get_track_uri(spotify=spotify, name='come up'))
# spotify.pause_playback(device_id=get_device_id())



while True:
    spotify_request(input("Command: "))

