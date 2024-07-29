# Advanced Chess Engine

## Overview

The **Advanced Chess Engine** is a high-performance chess engine designed to provide challenging gameplay and a solid foundation for further development. This engine supports the Universal Chess Interface (UCI) protocol, allowing it to be integrated with various chess graphical user interfaces (GUIs) and tools.

## Features

- Supports UCI protocol for easy integration with GUIs.
- Implements fundamental chess rules and move validation.
- Basic move generation and simple best-move selection.
- Customizable to support more advanced algorithms and features.

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/VANSHTalyani/chess_game
    ```

2. **Install the engine**:

    Use the `setup.py` script to install the engine:

    ```bash
    python setup.py install
    ```

## Usage

To run the engine, execute the script directly from the command line:

```bash
python engine.py


To start a new game and let the engine suggest a move, run:
python3 engine.py

Then enter the following commands:(To check whether the engine works properly or not)
uci
isready
ucinewgame
position startpos
go
