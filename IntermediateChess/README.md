README.md
MarkDown
# Chess Game Application

A web-based chess game application built using Flask, HTML, CSS, and JavaScript.

## Features

*   Chess game logic implementation
*   Board representation using 2D array
*   Piece representation using objects
*   Move validation and execution
*   User-friendly interface with board display and piece display
*   Move input using click events
*   Move validation feedback and check/checkmate detection
*   Undo/redo functionality and valid move highlighting
*   Piece promotion and draw detection
*   Game over message display

## Requirements

*   Python 3.8+
*   Flask 2.0+
*   Flask-Login 0.5+
*   Flask-Caching 1.10+
*   Flask-Security-Too 4.1.0

## Installation

1.  Clone the repository using `git clone https://github.com/your-username/your-repo-name.git`
2.  Navigate to the project directory using `cd your-repo-name`
3.  Create a virtual environment using `python -m venv venv`
4.  Activate the virtual environment using `source venv/bin/activate` (on Linux/Mac) or `venv\Scripts\activate` (on Windows)
5.  Install the required dependencies using `pip install -r requirements.txt`
6.  Run the application using `python app.py`

## Usage

1.  Open a web browser and navigate to `http://localhost:5000`
2.  Play the game by clicking on the pieces and squares to make moves
3.  Use the undo and redo buttons to navigate through the game history
4.  View the game over message when the game is completed
