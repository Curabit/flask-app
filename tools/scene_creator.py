import json
import os
import sys

def get_scene_details(scene_name='root'):
    print("\n\nOption Name: "+scene_name)
    scene = dict()
    scene["fname"] = input("Enter filename: ")
    scene["isLooped"] = False
    scene["isBranched"] = False
    if (input("Is this scene looped? Y/N: ") in ["Y","y"]):
        scene["isLooped"] = True
    elif (input("Does this scene branch further? Y/N: ") in ["Y","y"]):
        scene["isBranched"] = True
        scene["prompt"] = input("Enter the prompt to be displayed: ")
        options = input("Enter the choices offered: ").split()
        scene["branches"] = dict()
        for option in options:
            scene["branches"][option] = get_scene_details(option)
    return scene

json_object = json.dumps(get_scene_details, indent = 4)
  
isReadyToExport = False
while(not isReadyToExport):
    fname = input("\n\nEnter the filename: ")
    
    if (os.path.isfile('./'+fname+'.json')):
        print("A JSON file of a previous scene already exists. Move that file and try again or choose a new name.")
    else:
        isReadyToExport = True

with open((fname+".json"), "w") as outfile:
    outfile.write(json_object)