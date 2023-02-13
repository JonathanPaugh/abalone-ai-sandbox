# Abalone AI Sandbox
> An AI agent for the game of [Abalone](https://en.wikipedia.org/wiki/Abalone_(board_game))

This program is an ongoing project built by Team 4 for COMP 3981 (Artificial Intelligence and Machine Learning) at BCIT during the Winter 2022 semester.

## Overview
The goal of our project is to develop an Abalone agent capable of playing against and defeating a human player.

The primary functions of this program are to allow a user to play a game of Abalone against a CPU opponent or to allow two users to play against each other.

## Game installation and instructions
Download and run `Abalone.exe` from the release under [Releases](https://github.com/JonathanPaugh/COMP3981-Team4/releases) > Assets.

## State generator installation and instructions
1. Download `StateGenerator.exe` from the latest release under [Releases](https://github.com/JonathanPaugh/COMP3981-Team4/releases) > Assets.
2. Drag and drop the `Test<#>.input` files onto the executable.
3. A `dist/` folder will be created in the same directory containing the output files for all the given input files.

For more information on the state generator, view the state generator [README](https://github.com/JonathanPaugh/COMP3981-Team4/tree/main/parse/README.md).

## Development
The GUI for this project has been prebuilt for Windows. To build the application locally, use [pyinstaller](https://pypi.org/project/pyinstaller/).
```sh
> py -m PyInstaller -Fwn Abalone src/app.py
> py -m PyInstaller -Fwn StateGenerator src/tester.py
```

## Contributors
- Jonathan Paugh ([JonathanPaugh](https://github.com/JonathanPaugh))
- Jeff Phan ([jeffphan99](https://github.com/jeffphan99))
- Angela Qi ([angela-qi](https://github.com/angela-qi))
- Brandon Semilla ([semibran](https://github.com/semibran))
