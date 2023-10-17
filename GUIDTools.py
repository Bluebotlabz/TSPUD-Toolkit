from tqdm import tqdm
from os import path
import yaml
import os


def replaceGUIDs(guidReplacements: dict, projectroot: str, dryRun=False):
    ###
    # Fix guid references
    ###
    projectFiles = []
    print("\nFixing GUID References...")
    for root, dirs, files in os.walk(projectroot):
        if ('Mesh\\' in root or 'Mesh/' in root or 'Texture2D\\' in root or 'Texture2D/' in root):
            continue # Skip folder

        for fileName in files:
            if (fileName.split('.')[-1] in ['asset', 'prefab', 'unity', 'mat']):
                projectFiles.append(path.join(root, fileName))


    ###
    # Replace file contents
    ###
    progressBar = tqdm(total=len(projectFiles))
    for filePath in projectFiles:
        if (dryRun):
            replacements = []
            with open(filePath, 'rb+') as file:
                fileContents = file.read()
                for guidReplacement in guidReplacements.keys():
                    if (guidReplacement.encode('ascii') in fileContents):
                        replacements.append(guidReplacement)
                        
            if (len(replacements) > 0):
                print(filePath)
                for replacement in replacements:
                    print(replacement, '->', guidReplacements[replacement])
                print()
        else:
            with open(filePath, 'rb+') as file:
                originalFileContents = file.read()
                replacedFileContents = originalFileContents
                for guidReplacement in guidReplacements.keys():
                    replacedFileContents = replacedFileContents.replace(guidReplacement.encode('ascii'), guidReplacements[guidReplacement].encode('ascii'))

                if replacedFileContents != originalFileContents:
                    progressBar.write("Updated GUIDs in " + filePath)
                    file.seek(0, 0)
                    file.write(replacedFileContents)
                    file.truncate(file.tell())

        progressBar.update(1)

    progressBar.close()



def listGUIDs(metaPath: str, recursive: bool = False, pathWhitelist: list = ["meta"]):
    projectFiles = []

    if (recursive):
        for root, dirs, files in os.walk(metaPath):
            if ('Mesh\\' in root or 'Mesh/' in root or 'Texture2D\\' in root or 'Texture2D/' in root):
                continue # Skip folder

            for fileName in files:
                if (fileName.split('.')[-1] in pathWhitelist):
                    projectFiles.append(path.join(root, fileName))
    else:
        projectListing = os.listdir(metaPath)
        for item in projectListing:
            if (path.isfile(item)):
                projectFiles.append(projectListing)


    fileGUIDs = {}
    for filePath in projectFiles:
        with open(filePath, 'r') as metaFile:
            metadata = yaml.safe_load(metaFile.read())
            fileGUIDs[path.split(filePath)[-1]] = metadata['guid']

    return fileGUIDs