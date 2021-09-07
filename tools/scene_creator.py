import json
import os
import sys
from datetime import datetime

videos = []

def get_scene_details(pre="", scene_name='root'):
    global videos
    print("\n\nScene/Option Name: "+pre+"->"+scene_name)
    if pre=="":
        new_pre = scene_name
    else:
        new_pre = pre+"->"+scene_name
    scene = dict()
    scene["name"] = scene_name
    scene["fname"] = input("Enter filename of video: ")
    if scene['fname'] not in videos:
        videos.append(scene['fname'])
    scene["duration"] = input("Enter duration of video (MM:SS): ")
    scene["isLooped"] = False
    scene["isBranched"] = False
    if (input("Is this scene looped? Y/N: ") in ["Y","y"]):
        scene["isLooped"] = True
    elif (input("Does this scene branch further? Y/N: ") in ["Y","y"]):
        scene["isBranched"] = True
        scene["prompt_question"] = input("Enter the prompt to be displayed: ")
        scene["prompt_timestamp"] = input("Enter timestamp to show prompt at (MM:SS): ")
        options = input("Enter the choices offered (split by |): ").split('|')
        scene["default_choice"] = input("Enter default option (in case of no selection): ")
        scene["branches"] = list()
        for option in options:
            scene["branches"].append(get_scene_details(new_pre, option))
    return scene

# json_object = json.dump(get_scene_details(), indent = 4)
fname = ""
while(True):
    fname = input("\n\nEnter the filename to save JSON in: ")
    
    if (os.path.isfile('./'+fname+'.json')):
        print("A JSON file of a previous scene already exists. Move that file and try again or choose a new name.")
    else:
        break

_json = {
    "flow": get_scene_details(),
    "videos": videos
}

with open((fname+".json"), "w") as outfile:
    json.dump(_json, outfile, indent=4)