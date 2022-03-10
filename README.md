# COMP3981-Team4
> An AI agent for the game of [Abalone](https://en.wikipedia.org/wiki/Abalone_(board_game))

This program is an ongoing project built by Team 4 for COMP 3981 (Artificial Intelligence and Machine Learning) at BCIT during the Winter 2022 semester.

## Overview
The goal of our project is to develop an Abalone agent capable of playing against and defeating a human player.

The primary functions of this program are to allow a user to play a game of Abalone against a CPU opponent or to allow two users to play against each other.

## Game Installation
Download and run `Abalone.exe` from the release under [Releases](https://github.com/JonathanPaugh/COMP3981-Team4/releases) > Assets.

## State Generator Installation and Instructions
1. Download `StateGenerator.exe` from the latest release under [Releases](https://github.com/JonathanPaugh/COMP3981-Team4/releases) > Assets.
2. You will need a folder named 'input' which contains test boards named Test<#>.input.
3. You must run the executable at the same directory level as the 'input' folder. We recommend putting them both in the same folder.
4. The executable should run, and a 'dist' folder will be created containing the output files.

## Development
The GUI for this project has been prebuilt for Windows. To build the application locally, use [pyinstaller](https://pypi.org/project/pyinstaller/).
```sh
> py -m PyInstaller -Fwn Abalone src/ui.py
```

## Contributors
- Jonathan Paugh ([JonathanPaugh](https://github.com/JonathanPaugh))
- Jeff Phan ([jeffphan99](https://github.com/jeffphan99))
- Angela Qi ([angela-qi](https://github.com/angela-qi))
- Brandon Semilla ([semibran](https://github.com/semibran))
