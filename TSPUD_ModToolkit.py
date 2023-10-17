from unitypackage_extractor.extractor import extractPackage
from os import path
import GUIDTools
import requests
import shutil
import yaml
import os

def executeCommand(command, args):
    execute = command
    for arg in args:
        if (' ' in arg):
            execute += ' "' + arg + '"'
        else:
            execute += ' ' + arg

    os.system(execute)


def ScriptSync(scriptsPath: str, packagePath: str, projectRoot: str, recursive:bool = True, dryrun:bool = False):
    ###
    # Go through the inputpath and build a list of *.meta files
    ###
    print("Searching for Meta Files...")
    scriptGUIDs = GUIDTools.listGUIDs(scriptsPath, recursive)

    guidReplacements = {}
    print("Matching Meta Files...")
    packageGUIDs = GUIDTools.listGUIDs(packagePath, recursive)

    for fileName in packageGUIDs.keys():
        if (fileName in scriptGUIDs.keys() and fileName != 'AssemblyInfo.cs.meta'):
            guidReplacements[scriptGUIDs[fileName]] = packageGUIDs[fileName]
            print("GUID Mapping:", fileName, '-', scriptGUIDs[fileName], '->', packageGUIDs[fileName])

    GUIDTools.replaceGUIDs(guidReplacements, projectRoot, dryrun)


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



versionString = "v0.3.5"

projectRoot = "../TSPUD_UnityProject/"
packages = { # Key is package ID as in the PackageCache folder, and the value is the source location to get scripts from
     "com.malee.reorderablelist":  "Assets/Scripts/Malee.ReorderableList/",
     "com.unity.textmeshpro":  "Assets/Scripts/Unity.TextMeshPro/",
     "com.olegknyazev.softmask": "Assets/Scripts/SoftMask/"
}

config = {
    "FixPackageGUIDs": True,
    "FixProBuilderGUIDs": True,
    "FixTMPShaders": True,
    "FixSoftMaskShaders": True,
    "FixSoftMaskSamples": True,
    "FixAmplifyColour": True,
    "FixAmplifyBloom": True,
    "FixScripts": True
}

print("=================================")
print("= TSPUD Modkit Generator Script =")
print("= ALPHA                         =")
print("=                               =")
print("=          Created By:          =")
print("= thatHackerDudeFromCyberspace  =")
print("=        aka: Bluebotlabz       =")
print("=                               =")
print("======================= " + versionString + "  =")

os.makedirs('./tmp/', exist_ok=True)

print("\n\n")
print("Make sure you have opened the project in Unity and installed the following packages:")
print("> com.unity.ugui")
print("> com.unity.probuilder")
for package in packages.keys():
    print(">", package)
input("\nPress [ENTER] to continue >>> ")



###
# Fix package scripts
###
if (config["FixPackageGUIDs"]):
    for packageID in packages.keys():
        print("\n\nFixing GUIDs for:", packageID)

        # Find package folder
        for packageFolder in os.listdir(path.join(projectRoot, "Library/PackageCache/")):
            if (packageFolder.split('@')[0] == packageID):
                print("Found:", packageFolder)
                break

        # Replace package folder GUIDs and then delete the script folder (as it is no longer needed)
        ScriptSync(path.join(projectRoot, packages[packageID]), path.join(projectRoot, "Library/PackageCache/", packageFolder), projectRoot, True, False)
        shutil.rmtree(path.join(projectRoot, packages[packageID]))
        print("Deleted:", path.join(projectRoot, packages[packageID]))


    print("\n\n")
    print("Please re-open Unity and Import TMP Essential Resources via the menu:")
    print("Window > TextMeshPro > Import TMP Essential Resources")
    print("\nThen close Unity")
    input("\nPress [ENTER] to continue >>>")



if (config["FixProBuilderGUIDs"]):
    for packageFolder in os.listdir(path.join(projectRoot, "Library/PackageCache/")):
        if (packageFolder.split('@')[0] == "com.unity.probuilder"):
            print("Found:", packageFolder)
            break

    print("\n\nFixing GUIDs for: Probuilder")

    proBuilderPaths = {
        path.join(projectRoot, "Assets/Scripts/Unity.ProBuilder/"): path.join(projectRoot, "Library/PackageCache/", packageFolder, "Runtime/"),
        path.join(projectRoot, "Assets/Scripts/Unity.ProBuilder.Csg/"): path.join(projectRoot, "Library/PackageCache/", packageFolder, "External/CSG"),
        path.join(projectRoot, "Assets/Scripts/Unity.ProBuilder.KdTree/"): path.join(projectRoot, "Library/PackageCache/", packageFolder, "External/KdTree"),
        path.join(projectRoot, "Assets/Scripts/Unity.ProBuilder.Stl/"): path.join(projectRoot, "Library/PackageCache/", packageFolder, "External/StlExporter"),
        path.join(projectRoot, "Assets/Scripts/Unity.ProBuilder.Poly2Tri/"): path.join(projectRoot, "Library/PackageCache/", packageFolder, "External/Poly2Tri")
    }
    guidReplacements = {}

    for scriptsPath in proBuilderPaths.keys():
        ###
        # Go through the inputpath and build a list of *.meta files
        ###
        print("Searching for Meta Files...")
        scriptGUIDs = GUIDTools.listGUIDs(scriptsPath, True)

        print("Matching Meta Files...")
        packageGUIDs = GUIDTools.listGUIDs(proBuilderPaths[scriptsPath], True)

        for fileName in packageGUIDs.keys():
            if (fileName in scriptGUIDs.keys() and fileName != 'AssemblyInfo.cs.meta'):
                guidReplacements[scriptGUIDs[fileName]] = packageGUIDs[fileName]
                print("GUID Mapping:", fileName, '-', scriptGUIDs[fileName], '->', packageGUIDs[fileName])
    
    GUIDTools.replaceGUIDs(guidReplacements, projectRoot)
    
    shutil.rmtree(path.join(projectRoot, "Assets/Scripts/Unity.ProBuilder/"))
    shutil.rmtree(path.join(projectRoot, "Assets/Scripts/Unity.ProBuilder.Csg/"))
    shutil.rmtree(path.join(projectRoot, "Assets/Scripts/Unity.ProBuilder.KdTree/"))
    shutil.rmtree(path.join(projectRoot, "Assets/Scripts/Unity.ProBuilder.Stl/"))
    shutil.rmtree(path.join(projectRoot, "Assets/Scripts/Unity.ProBuilder.Poly2Tri/"))

    print("Probuilder GUIDs Fixed!")



###
# Fix TMP Shaders
###
if (config["FixTMPShaders"]):
    print("Fixing TextMeshPro Shaders...")

    print("Searching for TMP Shader Files...")
    targetIDs = getShaderGUIDs(path.join(projectRoot, "Assets/Shader/"))
    sourceIDs = getShaderGUIDs(path.join(projectRoot, "Assets/TextMesh Pro/Shaders"))

    guidReplacements = {}
    print("\nMatching TMP Shader Files...")
    for shaderName in sourceIDs:
        if (shaderName in targetIDs.keys()):
            print("GUID Mapping:", shaderName, '-', targetIDs[shaderName][0], '->', sourceIDs[shaderName][0])
            guidReplacements[targetIDs[shaderName][0]] = sourceIDs[shaderName][0]

    GUIDTools.replaceGUIDs(guidReplacements, projectRoot, False)



###
# Fix SoftMask Shaders
###
if (config["FixSoftMaskShaders"]):
    print("Fixing SoftMask Shaders...")

    for packageFolder in os.listdir(path.join(projectRoot, "Library/PackageCache/")):
        if (packageFolder.split('@')[0] == "com.olegknyazev.softmask"):
            print("Found:", packageFolder)
            break

    print("Searching for SoftMask Shader Files...")
    targetIDs = getShaderGUIDs(path.join(projectRoot, "Assets/Resources/"))
    sourceIDs = getShaderGUIDs(path.join(projectRoot, "Library/PackageCache/", packageFolder, "Assets/Shaders/Resources/"))

    guidReplacements = {}
    shaderPaths = []
    print("\nMatching SoftMask Shader Files...")
    for shaderName in sourceIDs:
        if (shaderName in targetIDs.keys()):
            print("GUID Mapping:", shaderName, '-', targetIDs[shaderName][0], '->', sourceIDs[shaderName][0])
            guidReplacements[targetIDs[shaderName][0]] = sourceIDs[shaderName][0]
            shaderPaths.append(targetIDs[shaderName][1])

    GUIDTools.replaceGUIDs(guidReplacements, projectRoot, False)

    for shaderPath in shaderPaths:
        print("Deleting:", shaderPath)
        os.remove(shaderPath)



###
# Fix SoftMask Sample Scripts
###
if (config["FixSoftMaskSamples"]):
    print("Fixing SoftMask Sample Scripts...")

    for packageFolder in os.listdir(path.join(projectRoot, "Library/PackageCache/")):
        if (packageFolder.split('@')[0] == "com.olegknyazev.softmask"):
            print("Found:", packageFolder)
            break

    ScriptSync(path.join(projectRoot, "Assets/Scripts/Assembly-CSharp/SoftMasking/Samples/"), path.join(projectRoot, "Library/PackageCache/", packageFolder, "Samples~/Scripts/"), projectRoot, True, False)
    shutil.rmtree(path.join(projectRoot, "Assets/Scripts/Assembly-CSharp/SoftMasking/"))



###
# Get Amplify Colour Shaders
###
if (config["FixAmplifyColour"]):
    print("Fixing Amplify Color...")
    os.system("git clone https://github.com/AmplifyCreations/AmplifyColor.git ./tmp/AmplifyColor")

    print("Deleting broken Amplify Colour Shaders...")
    for fileName in os.listdir(path.join(projectRoot, "Assets/Resources/")):
        if (fileName[:20] == "Hidden_Amplify Color"):
            os.remove(path.join(projectRoot, "Assets/Resources/", fileName))

    print("Copying working Amplify Colour Shaders...")
    for fileName in os.listdir("./tmp/AmplifyColor/Assets/AmplifyColor/Resources/"):
        shutil.copy(path.join("./tmp/AmplifyColor/Assets/AmplifyColor/Resources/", fileName), path.join(projectRoot, "Assets/Resources/"))
    
    print("Amplify Color Fixed!")


###
# Get Amplify Bloom Shaders
###
if (config["FixAmplifyBloom"]):
    print("Fixing Amplify Bloom...")

    print("Downloading Amplify Bloom...")
    response = requests.get("http://amplify.pt/wp-content/download/AmplifyBloomTrial.zip", stream=True)
    with open("./tmp/AmplifyBloomTrial.zip", 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024):
            file.write(chunk)

    print("Extracting Amplify Bloom")
    shutil.unpack_archive("./tmp/AmplifyBloomTrial.zip", "./tmp/AmplifyBloomTrial/")
    extractPackage("./tmp/AmplifyBloomTrial/AmplifyBloomTrial_Unity5.unitypackage", outputPath="./tmp/AmplifyBloomTrial/ExtractedPackage/")
    
    print("Deleting broken Amplify Bloom Shaders...")
    os.remove(path.join(projectRoot, "Assets/Resources/Hidden_AmplifyBloom.shader"))
    os.remove(path.join(projectRoot, "Assets/Resources/Hidden_AmplifyBloom.shader.meta"))
    os.remove(path.join(projectRoot, "Assets/Resources/Hidden_BloomFinal.shader"))
    os.remove(path.join(projectRoot, "Assets/Resources/Hidden_BloomFinal.shader.meta"))

    print("Copying working Amplify Bloom Shaders...")
    for fileName in os.listdir("./tmp/AmplifyBloomTrial/ExtractedPackage/Assets/AmplifyBloom/Resources/"):
        shutil.copy(path.join("./tmp/AmplifyBloomTrial/ExtractedPackage/Assets/AmplifyBloom/Resources/", fileName), path.join(projectRoot, "Assets/Resources/"))

    print("Amplify Bloom Fixed!")

print("\n\n\n")
print("===================================================================")
print("=                       UNITY PROJECT FIXED!                      =")
print("=  You can now open the project and mod to your heart's content!  =")
print("=                                                                 =")
print("=                           Created By:                           =")
print("=                  thatHackerDudeFromCyberspace                   =")
print("=                         aka: Bluebotlabz                        =")
print("=                                                                 =")
print("===================================================================")