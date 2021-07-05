import sys
import json




#Update and write dictionary to file
dic1 = {"a": 1, "b": 2}
dic2 = {"c": 3, "d": 4}

todo = {}

print(dic1)
print(dic2)
dic1.update(dic2)
print(dic1)

f = open('files/todo.json', 'w')
json.dump(dic1, f)
f.close()


#pop key
f = open('files/todo.json', 'r')
data = json.load(f)
data.pop('d', None)
print(data)
f.close()


print("")
print("")


with open("files/todo1.json", "r") as f:

    data = json.load(f)

    print(data['first'][1]['name'])

    print(data['third'][0])

    print(data['fourth'])
try:
    with open("files/todo1.json", "w") as f:
        print("")
        print(data["to-do"])
        print(data["to-do"][0])
        print(data["to-do"][0]["task"])

        data["to-do"].append({"task":"nice"}) # adds new dict in list
        data["to-do"][0]["task"] = "new task added" # adds new key to dict in list
        data["to-do"][0].pop("task", None) # pops key in dict in list
        data["to-do"][0].clear() # clears values in dict
        data["to-do"].pop(0) # pops dict from list

        print(data["to-do"][0])

        json.dump(data, f, indent = 4)

        for task in data["to-do"]:
            print(task["task"])

except:
    pass


with open("files/todo_list.json", "r") as f:
    data = json.load(f)

with open("files/todo_list.json", "w") as f:
    #task input
    task = input("Task: \n")
    count = 0
    #counts amount of tasks
    for tsk in data["to-do"][0]:
        print(data["to-do"][0])
        count += 1
    #adds new task 
    data["to-do"][0]["task" + str(count + 1)] = str(task)
    #json.dump(data, f, indent = 4)

    #prints all the tasks
    # for tsk in data["to-do"][0]:
    #     print(data["to-do"][0][tsk])

    
    # Removes 'task' from dict
    task_remove = input("task to remove: ")
    if task_remove != "no":
        data["to-do"][0].pop("task" + str(task_remove), None)

        count = 1

        for key, val in list(data["to-do"][0].items()):
            print(key)
            if key == "task" + str(count):
                pass
            elif key == "task" + str(count + 1):
                data["to-do"][0]["task" + str(count)] = data["to-do"][0][key]
                del data["to-do"][0][key]
                
            count += 1

    else:
        pass

        


    json.dump(data, f, indent = 4)


# {
#     "to-do": [
#         {
#             "task": "Adrian"
#         },
#         {
#             "task": "Adriana"
#         }
#     ]
# }
