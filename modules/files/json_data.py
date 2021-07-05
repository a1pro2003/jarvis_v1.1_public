import sys
import json
import csv
from pathlib import Path
from tempfile import NamedTemporaryFile
import shutil
import os
import psutil
import subprocess
from os.path import expanduser


current_dir_path = str(os.path.dirname(os.path.realpath(__file__)))
user_dir_path = str(Path.home())
home = expanduser("~")
modules_files = '\\modules\\files'


def task_list(): #DONE
    #opens json file, stores data and returns the list
    with open(current_dir_path + "\\todo_list.json", "r") as f:
        data = json.load(f)
    
    task_list = data["to-do"][0]

    return task_list

def task_add(new_task): #DONE
    #opens, reads and stores data
    with open(current_dir_path + "\\todo_list.json", "r") as f:
        data = json.load(f)

    #counts number of tasks to keep track and adds a new task to the end
    with open(current_dir_path + "\\todo_list.json", "w") as f:
        #counts amount of tasks
        count = 0
        for tsk in data["to-do"][0]:
            print(data["to-do"][0])
            count += 1

        #adds new task
        data["to-do"][0]["task" + str(count + 1)] = str(new_task)
        #dumps data to json file
        json.dump(data, f, indent = 4)

def task_delete(task): #DONE
    #opens, reads and stores data
    with open(current_dir_path + "\\todo_list.json", "r") as f:
        data = json.load(f)

    old_data = data

    with open(current_dir_path + "\\todo_list.json", "w") as f:
        try:
            #checks that the input does not contain a 'no' and that the item requested is in the list
            if task != "no" and ("task" + str(task)) in data["to-do"][0]:
                data["to-do"][0].pop("task" + str(task), None)

                count = 1
                #iterates through list and checks the key position
                for key, val in list(data["to-do"][0].items()):
                    print(key)
                    #checks that the key is in the right position
                    if key == "task" + str(count):
                        pass
                    #if the key is in the wrong position it updates it
                    elif key == "task" + str(count + 1):
                        data["to-do"][0]["task" + str(count)] = data["to-do"][0][key]
                        del data["to-do"][0][key]
                        
                    count += 1
                #dumps json data
                json.dump(data, f, indent = 4)

            #if requested task is not in list returns False
            elif ("task" + str(task)) not in data["to-do"][0]:
                json.dump(old_data, f, indent = 4)
                return False
            else:
                pass

        except ValueError:
            print(ValueError)

def data_csv(): #DONE

    with open(current_dir_path + "/data.csv", "r") as f:      
        data = csv.reader(f, delimiter=',')
        line_count = 0
        for row in data:
            if line_count == 0:
                print("Coloumb names are: {}".format(", ".join(row)))
                line_count += 1
            else:
                print(row[0] + row[1])
            
            if row[0] == 'intents_size':
                print(row[1])

def get_intents_size():
    with open(current_dir_path + "/data.csv", "r") as f:
        data = csv.reader(f, delimiter=',')
        line_count = 0

        for row in data:
            if row[0] == 'intents_size':
                return int(row[1])
            else:
                pass

def write_intents_size():

    fields = ['key', 'data']
    tempfile = NamedTemporaryFile(mode='w', delete=False, newline='')

    with open(current_dir_path + "/data.csv", "r") as inn,tempfile:
        reader = csv.DictReader(inn, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)

        for row in reader:

            if row['key'] == 'intents_size':
                row['data'] = int(Path(current_dir_path + '\\intents.json').stat().st_size)
                row = {'key' : row["key"], 'data' : row['data']}
            writer.writerow(row)
    shutil.move(tempfile.name, current_dir_path + "/data.csv")
    return True

def intents_size():
    return int(Path(current_dir_path +'\\intents.json').stat().st_size)

def test():
    return (current_dir_path + "\\todo_list.json")

#print(test())
    
