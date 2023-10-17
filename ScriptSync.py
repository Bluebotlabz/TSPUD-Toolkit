from tqdm import tqdm
from os import path
import argparse
import GUIDTools
import pathlib
import yaml
import os



###
# Arguments
###
parser = argparse.ArgumentParser(
                    prog='MetaSync',
                    description='Locate and replace Unity Script Meta files from one location to another',
                    epilog='')

parser.add_argument('scriptpath', type=pathlib.Path, help="The path contianing *.meta files of GUIDs to target")
parser.add_argument('packagepath', type=pathlib.Path, help="The path containing *.meta files of GUIDs to replace with")
parser.add_argument('projectroot', type=pathlib.Path, help="The project root")
parser.add_argument('-d', '--dry', action='store_true', help="Preview command output, does not actually replace files")

args = parser.parse_args()



if (args.dry):
    print("DRY-RUN MODE, no filesystem changes will be made\n\n\n")


###
# Go through the inputpath and build a list of *.meta files
###
print("Searching for Meta Files...")
scriptGUIDs = GUIDTools.listGUIDs(args.scriptpath, True)


guidReplacements = {}
destMatchFails = []
print("\nMatching Meta Files...")
packageGUIDs = GUIDTools.listGUIDs(args.packagepath, True)

for fileName in packageGUIDs.keys():
    if (fileName in scriptGUIDs.keys() and fileName != 'AssemblyInfo.cs.meta'):
        guidReplacements[scriptGUIDs[fileName]] = packageGUIDs[fileName]
        print("GUID Mapping:", fileName, '-', scriptGUIDs[fileName], '->', packageGUIDs[fileName])


GUIDTools.replaceGUIDs(guidReplacements, args.projectroot, args.dry)



if (args.dry):
    print("\n\nDry-run complete!")
    print("Check output before running!")
else:
    print("\n\nMeta Files Replaced!")
    print("You can now delete:", args.srcpath)