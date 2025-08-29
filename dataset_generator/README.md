# SpeedSolving-Master Modification for Dataset Generation

SpeedSolving-Master is a great app made by German Ramos to solve Rubik's cubes with different speedsolving methods, which made this dataset generation possible with a few tweaks to the app and a little bit of python parsing.

**Disclaimer: This setup was made for Mac and may or may not work on other operating systems.**

## Setup App

#### Install dependencies

Install Homebrew if not already installed

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Install Qt5 (newer versions may break older code)

```bash
brew install qt@5
```

Make sure the tools are in the PATH:

```bash
echo 'export PATH="/usr/local/opt/qt@5/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

#### Build and compile the project with qmake

```bash
cd SpeedSolving-Master
qmake SSMaster.pro
make
```

#### Open the app

```bash
./SSMaster.app/Contents/MacOS/SSMaster
```

## Setup Python

Create virtual environment; ideally inside dataset_generator (--copies is for externally managed systems like homebrew)

```bash
python3 -m venv --copies myenv
source myenv/bin/activate
```

Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

Make sure to select the interpreter from the `myenv` folder
In VSCode, this means running the `Python: Select Interpreter` command and selecting starting with `./myenv/`

## Generation

Within the app, select the desired `Method` and `Number of Scrambles` from the dropdowns. Then, click `Start` and wait for the process to finish (the last solution should be displayed then). Then, click `Export History` and select the `dataset_generator/exports` folder (in order to run `parse.py`). Repeat for all desired methods. Keeping the app running to export everything at once is ideal; if not the jsons must be combined manually.

## Parsing

To parse the exported json, simply update the files names in `parse.py` to match desired input and output locations and run the file.
