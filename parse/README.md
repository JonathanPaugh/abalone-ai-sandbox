# Abalone State Generator
This repository contains a state generator as part of the deliverable for Part 2 of the term project. It receives an `.input` file denoting the initial board configuration and whose turn it is to move and generates a list of moves (`.move` file) and a list of board configurations (`.board` file) that can arise from the given input position.

## Installation and instructions
1. Download `StateGenerator.exe` from the latest release under [Releases](https://github.com/JonathanPaugh/COMP3981-Team4/releases) > Assets.
2. Drag and drop the `Test<#>.input` files onto the executable.
3. A `dist/` folder will be created in the same directory containing the output files for all the given input files.

## Input formats
The `.input` file that the state generator operates on must conform to the following format:
```
b
C5b,D5b,E4b,E5b,E6b,F5b,F6b,F7b,F8b,G6b,H6b,C3w,C4w,D3w,D4w,D6w,E7w,F4w,G5w,G7w,G8w,G9w,H7w,H8w,H9w
```
where:
- the first line denotes whose turn it is to move (`b` for black and `w` for white)
- the second line denotes a `board configuration` via a `piece` list -- each comma-separated piece consists of a `cell` (in Abalone notation, e.g. `C5`) and a `color` (`b`/`w`); cells that are omitted from the piece list are assumed to be empty.

## Output formats
A `.move` file enumerates all possible moves that are legal given the input position. A `move` is written as a `(direction, start[, end])` tuple where:
- `direction` denotes a cardinal direction in hexagonal space e.g. (`NW`, `NE`, `W`, `E`, `SW`, `SE`)
- `start` denotes the "starting" cell for the selection line of marbles to be moved, e.g. `A1`
- `end` denotes the "ending" cell for the selection line of marbles to be moved, e.g. `C3`; may be omitted for single marble moves.

A `.board` file enumerates all possible board configurations that can arise from the given input position. The syntax that denotes for each board is identical to the syntax for board configurations used in `.input` files (i.e. not including turn).
