# TSPUD-Toolkit

A series of Python scripts designed to fix a decompiled version of TSPUD so that it can be recompiled.

Note: this is a very early Alpha, help is appreciated to improve these scripts

~~~
THIS PROJECT HAS BEEN DISCONTINUED AS I DO NOT HAVE THE TIME OR MOTIVATION TO WORK ON IT
~~~


## What works?
- Running TSPUD in-editor
- TextMeshPro scripts working
- AmplifyBloom working
- AmplifyColour working

## What is still broken?
- Many shaders
- Portals
- Doors
- Triggers (all types appear to be broken)
- Sounds in many maps
- Most map logic

## Usage
~~~
Note:
The entire process of decompiling and fixing the decompiled game may take up to 4 hours
~~~

### Prerequisites
- Python 3.9+ must be installed
- Libraries in `requirements.txt` must be installed (use the command: `pip3 install -r requirements.txt`)
- Unity `2019.4.33f1` must be installed by installing `Unity Hub` and clicking on [this link](unityhub://2019.4.31f1/bd5abf232a62) or by downloading it from: [here](https://unity.com/releases/editor/archive)

### Decompilation and Usage
1. Use [AssetRipper](https://github.com/AssetRipper/AssetRipper/releases) (`v0.3.4.0` is tested and supported with this script)
    - Change `Script Export Format` from `Hybrid` to `Decompiled`
    - Export the `all files` to a folder
2. Clone this repository
3. Identify the `ExportedProject` folder
4. Edit the `TSPUD_ModToolkit.py` script (`line 71`) to point towards your `ExportedProject` folder
5. Run the script and follow the instructions
