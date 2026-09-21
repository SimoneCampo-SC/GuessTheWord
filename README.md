# Guess the Word

A command-line word-guessing game written in Python, built around adaptive word-family selection rather than committing to a single hidden word at the start of the game.

The project explores algorithmic decision-making, state management and heuristic scoring through an Evil Hangman-style game mechanic.

## How it works

At the start of each game, the program selects a word length between 4 and 12 characters and gives the player twice that number of rounds.

Instead of immediately selecting one fixed word, the game maintains a set of candidate words that remain compatible with the player's guesses. After each valid letter guess, candidate words are grouped into word families according to the resulting pattern.

The game then selects one of those families and continues with the remaining candidates.

## Difficulty modes

### Easy

Easy mode selects the word family containing the largest number of remaining candidate words.

### Hard

Hard mode evaluates the available word families using a weighted heuristic based on:

- 60% — number of candidate words in the family
- 30% — number of undiscovered character positions
- 10% — number of possible letters remaining across the candidate words

The family with the highest resulting weight is selected.

## Debug mode

A debug mode is also available.

When enabled, the program uses a small built-in dictionary and displays:

- the available word families;
- the heuristic weights assigned to them;
- the family selected for the next game state.

This makes the internal decision process easier to inspect.

## Technical concepts

The project demonstrates:

- Python object-oriented programming
- dictionary and set operations
- candidate-space reduction
- pattern matching
- heuristic scoring
- game-state management
- file handling
- command-line interaction

## Running the project

The project uses only the Python standard library and does not require external packages.

From the repository root:

```bash
python3 GuessTheWord.py
```

Choose either Easy or Hard mode when prompted.

You can also enter `D` when asked about debug mode to inspect the internal word-family selection process.

## Word list

The game uses `dictionary.txt` as its main word list.

The file contains 127,142 words and is treated as external input data rather than project-authored program logic. The original project did not document the provenance of the word list.

## Project context

This is an earlier algorithm-focused Python project preserved as part of my public engineering portfolio.

It demonstrates how a relatively simple command-line game can be modelled as a changing search space, with each player action reducing and reorganising the set of valid candidate states.
