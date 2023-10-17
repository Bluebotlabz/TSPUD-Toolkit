from tqdm import tqdm
from os import path
import GUIDTools
import argparse
import pathlib
import yaml
import os


def getShaderGUIDs(shadersPath: str, recursive: bool = True):
    shaderIDs = {}
    
    for root, dirs, files in os.walk(shadersPath):
        for fileName in files:
            if (fileName.split('.')[-1] == 'shader'):
                with open(path.join(root, fileName), 'r') as file:
                    shaderName = None
                    shaderLine = "\n"
                    while (not shaderName) and shaderLine != "":
                        shaderLine = file.readline()
                        strippedLine = shaderLine.strip().encode('ascii', 'ignore').decode('ascii', 'ignore')

                        if (strippedLine[:8] == 'Shader "'):
                            shaderName = strippedLine.split('"')[1]
                            break
                    
                    if (shaderName == None):
                        print("Error identifying:", fileName)
                        continue

                # Get GUID
                with open(path.join(root, fileName + '.meta'), 'r') as metaFile:
                    shaderMetaData = yaml.safe_load(metaFile.read())
                    shaderIDs[shaderName] = [shaderMetaData['guid'], path.join(root, fileName)]
    
    return shaderIDs



###
# Arguments
###
parser = argparse.ArgumentParser(
                    prog='ShaderSync',
                    description='Locate and replace Unity Script Meta files from one location to another',
                    epilog='')

parser.add_argument('shadertarget', type=pathlib.Path, help="The path containing *.shader files of GUIDs to target")
parser.add_argument('shadersource', type=pathlib.Path, help="The path contianing *.shader files of GUIDs to replace with")
parser.add_argument('projectroot', type=pathlib.Path, help="The project root")
parser.add_argument('-d', '--dry', action='store_true', help="Preview command output, does not actually replace files")

args = parser.parse_args()



if (args.dry):
    print("DRY-RUN MODE, no filesystem changes will be made\n\n\n")



###
# Go through the inputpath and build a list of *.meta files
###
print("Searching for Shader Files...")
targetIDs = getShaderGUIDs(args.shadertarget)
sourceIDs = getShaderGUIDs(args.shadersource)

guidReplacements = {}
print("\nMatching Shader Files...")
for shaderName in sourceIDs:
    if (shaderName in targetIDs.keys()):
        guidReplacements[targetIDs[shaderName][0]] = sourceIDs[shaderName][0]



GUIDTools.replaceGUIDs(guidReplacements, args.projectroot, args.dry)



if (args.dry):
    print("\n\nDry-run complete!")
    print("Check output before running!")
else:
    print("\n\nMeta Files Replaced!")
    print("You can now delete:")
    for shaderName in sourceIDs.keys():
        if (shaderName[shaderName] in guidReplacements.keys()):
            print(shaderName, '-', sourceIDs[shaderName][1])