import json
import os
import sys
from datetime import datetime

def get_scene_details(pre="", scene_name='root'):
    print("\n\nScene/Option Name: "+pre+"->"+scene_name)
    if pre=="":
        new_pre = scene_name
    else:
        new_pre = pre+"->"+scene_name
    scene = dict()
    scene["name"] = scene_name
    scene["fname"] = input("Enter filename of video: ")
    scene["duration"] = input("Enter duration of video (MM:SS): ")
    scene["isLooped"] = False
    scene["isBranched"] = False
    if (input("Is this scene looped? Y/N: ") in ["Y","y"]):
        scene["isLooped"] = True
    elif (input("Does this scene branch further? Y/N: ") in ["Y","y"]):
        scene["isBranched"] = True
        scene["prompt_question"] = input("Enter the prompt to be displayed: ")
        scene["prompt_timestamp"] = input("Enter timestamp to show prompt at (MM:SS): ")
        options = input("Enter the choices offered: ").split('|')
        scene["branches"] = dict()
        for option in options:
            scene["branches"][option] = get_scene_details(new_pre, option)
    return scene

# json_object = json.dump(get_scene_details(), indent = 4)
fname = ""
while(True):
    fname = input("\n\nEnter the filename to save JSON in: ")
    
    if (os.path.isfile('./'+fname+'.json')):
        print("A JSON file of a previous scene already exists. Move that file and try again or choose a new name.")
    else:
        break

with open((fname+".json"), "w") as outfile:
    json.dump(get_scene_details(), outfile, indent=4)