from os import read, write
from pathlib import Path

# from scapy.sendrecv import send
# from modules.tv_control import network
# from modules.tv_control import scanner
# from modules.tv_control.discovery import *    # Because I'm lazy, don't do this.
# from modules.tv_control.connection import *
# from modules.tv_control.controls import *
# from modules.tv_control.scanner import *

#testing
import network
import scanner
from discovery import *    # Because I'm lazy, don't do this.
from connection import *
from controls import *
from network import *
from scanner import *

from time import sleep
import socket
import os
import sys
from wakeonlan import send_magic_packet

current_dir_path = str(os.path.dirname(os.path.realpath(__file__)))
user_dir_path = str(Path.home())
home = os.path.expanduser("~")
modules_tv_control_dir = '\\modules\\tv_control'
current_dir_path = str(os.path.dirname(os.path.realpath(__file__)))


#checks if file is empty
def store_store():
    with open(current_dir_path +  "\\config.json", 'r') as read_obj:
        # read first character
        one_char = read_obj.read(1)
        # if not fetched then file is empty
        if not one_char:
           return True
#save client key
def write_store(store):
    with open(current_dir_path +  "\\config.json", 'w') as write_obj:
        write_obj.write(json.dumps(store))
        #data = json.dump(write_obj, write_obj)
#Load client key    
def load_store():
    with open(current_dir_path +  "\\config.json", 'r') as read_obj:
        data = json.loads(read_obj.read())
        return data

def check_ip_file_empty():
    with open(current_dir_path +  "\\ip.txt", 'r') as read_obj:
        # read first character
        size = os.stat(current_dir_path +  '\\ip.txt').st_size
        # if not fetched then file is empty
        if size == 0:
            return True
        else:
            return False

def check_host():
    with open(current_dir_path +  '\\ip.txt', 'r') as f:
        ip = f.read()
    socket.gethostname

def get_stored_ip():
    
    with open(current_dir_path +  '\\ip.txt', 'r') as f:
        ip_mac = f.read()
        return ip_mac[:-18]

def get_stored_mac():
    with open(current_dir_path +  '\\ip.txt', 'r') as f:
        ip_mac = f.read()
        return ip_mac[-17:]

client = None


def setup():
    global client
    if store_store():
        store = {}
    else:
        store = load_store()


    if check_ip_file_empty() == True:
        print('No IP saved')
        print('Scanning network')
        try:
            ip_list = scanner.scan('192.168.1.0/24')
        except:
            ip_list = scanner.scan('192.168.0.0/24')

        print('Network scanned: ' + str(ip_list))

        count = 0
        #Attempts to connect to tv
        try:
            for ip in ip_list:
                try:   
                    client = WebOSClient(ip['ip']) #Target ip
                    client.connect()
                    try:
                        for status in client.register(store):
                            if status == WebOSClient.PROMPTED:
                                print("Please accept the connect on the TV!")
                            elif status == WebOSClient.REGISTERED:
                                print("Registration successful!")
                                break
                        with open(current_dir_path +  '\\ip.txt', 'w') as f:
                            f.write(ip['ip'] + ',' + ip['mac'])
                            print('Ip saved')
                            print('Successfull Connection')
                            break
                    except:
                        pass
                except:
                    print('pass')
                    count += 1
                    continue
            if count == len(ip_list):
                print('No TV recognised')
                sys.exit()
        except:
            #sys.exit()
            pass
            

    elif check_ip_file_empty() == False:

        ip = get_stored_ip()
        mac = get_stored_mac()
        print('ip: ' + ip + ' mac :' + mac)

        print('Checking saved IP')
        print('Attempting to power on saved IP device')
        print(ip + ' ' + mac)
        send_magic_packet(mac, ip_address = ip)

        try:
            client = WebOSClient(ip) #Target ip
            client.connect()
            for status in client.register(store):
                if status == WebOSClient.PROMPTED:
                    print("Please accept the connect on the TV!")
                elif status == WebOSClient.REGISTERED:
                    print("Saved IP successful!")
                    break
        except:
                print('Saved IP failed')
                print('Scanning network')
                try:
                    ip_list = scanner.scan('192.168.1.0/24')
                except:
                    ip_list = scanner.scan('192.168.0.0/24')

                print('Network scanned: ' + str(ip_list))
                count = 0
                #Attempts to connect to tv
                for ip in ip_list:
                    try:
                        client = WebOSClient(ip['ip']) #Target ip
                        client.connect()
                        try:
                            for status in client.register(store):
                                if status == WebOSClient.PROMPTED:
                                    print("Please accept the connect on the TV!")
                                elif status == WebOSClient.REGISTERED:
                                    print("Registration successful!")
                                    break
                            with open(current_dir_path +  '\\ip.txt', 'w') as f:
                                f.write(ip['ip'] + ',' + ip['mac'])
                                print('Ip saved')
                                print('Successfull Connection')
                                break
                        except:
                            pass
                            
                    except:
                        print('pass')
                        count += 1
                        continue
                if count == len(ip_list):
                    print('No TV recognised, or Tv Off')
                    #sys.exit()

    try:
        print('Ip used: ' + str(ip['ip']))
    except:
        print('Ip used: ' + str(ip))





    #write
    write_store(store)
    print("Authentication completed!\n")


def response(status_of_call, payload):
    if status_of_call:
        # Successful response from TV.
        # payload is a dict or an object (see API details)
        print(payload)  # Successful response from TV
    else:
        # payload is the error string.
        print("Error message: ", payload)

count_one = 0

def tv_controls(control):
    global count_one
    # while count_one == 0:
    #     setup()
    #     count_one += 1
    setup()

    media = MediaControl(client)
    system = SystemControl(client)
    app_control = ApplicationControl(client)

    control = control.lower()
    control = control.split()

    try:
        if ' '.join(control[0:2]) == 'increase volume':
            for i in  range(15):
                media.volume_up(callback=response)
                
        elif ' '.join(control[0:2]) == 'decrease volume':
            for i in  range(15):
                media.volume_down(callback=response)

        elif control[0] == 'mute':
            media.mute(True, callback=response)

        elif ' '.join(control[0:2]) == 'un mute':
            media.mute(False, callback=response)

        elif control[0] == 'resume':
            media.play(callback=response)

        elif control[0] == 'pause':
            media.pause(callback=response)

        elif control[0] == 'notification':
            print(control[1:3])
            if ' '.join(control[1:3]) == 'power off':
                system.power_off(callback=response)
                pass
            elif ' '.join(control[1:3]) == 'power on':
                with open(current_dir_path +  '\\ip.txt', 'r') as f:
                    ip_mac = f.read()
                    ip = ip_mac[:-18]
                    mac = ip_mac[-17:]
                    print('ip: ' + ip + ' mac :' + mac)
                    send_magic_packet(mac, ip_address = ip)

            else:
                system.notify(' '.join(control[1:]), callback=response)

        elif control[0] == 'launch':
            application = ' '.join(control[1:]).lower()
            app_list = app_control.list_apps() #gets list of apps
            app = [x for x in app_list if application in x["title"].lower()][0]
            app_info = app_control.launch(app, callback=response)
            

        else:
            print('Unrecognised command')
    except:
        print('No command parsed')


send_magic_packet('00:51:ED:DE:2B:7B', ip_address = '192.168.1.118')
#Testing
# while True:
#     sleep(1.5)

#     tv_controls(input("Command: "))