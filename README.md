## ⚠️ Heads up
This is a personal project that may be updated as needed

It should be used as a starting point and reference, not expected to handle every use case.

## Summary
A simple Flask-based API that simulates keyboard and mouse inputs to control a Windows game window remotely.

## Features

- Programmatically sends keypresses and mouse clicks to a game window
- REST API interface for automation or remote control
- Supports both single key presses and toggle (hold/release) behavior
- Automatically focuses the game window before sending input

## Requirements

- Windows OS
- Python 3.8+
- The following Python packages:
  - `Flask`
  - `pywin32`
  - `pynput`

## Install dependencies:
```bash
pip install Flask pywin32 pynput
```

## Run
```bash
python ./input_server.py
```
