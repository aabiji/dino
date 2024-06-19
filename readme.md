## Dino

A clone of chrome's Dinosaur Game. This time
the game is controled by hand gestures. This project uses
mediapipe for the hand landmarking and pygame for the game.
Pretty cool I think!

Running:
1. [Install mediapipe](https://ai.google.dev/edge/mediapipe/framework/getting_started/install)
2. Setup project and run
   ```
   # Install uv
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Setup project
   git clone https://github.com/aabiji/dino.git && cd dino
   uv venv .venv
   source .venv/bin/activate
   uv pip install -r requirements.txt

   python3 src/main.py
   ```