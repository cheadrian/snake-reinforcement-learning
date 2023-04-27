# Snake game reinforcement learning
Example of a snake game ML with Ray RLlib, PyGame, and Gymnasium.

[Check out on this Medium article](https://faun.pub/building-the-perfect-a-i-game-player-using-ray-rllib-pytorch-and-gymnasium-cdb1d5624844?sk=93e8b3523ed5f77c29df3c98c1dc4077)

## Training
To train the network, check out the Ray_RLlib_PyGame_Snake_Gym_Training.ipynb notebook.

## Environement
In order to run these files, you need a Python environment with few libraries installed.

Check the `requirements.txt`.

Conda environment for Ray with Pytorch, Nivida GPU:

    conda create --name ray_torch python=3.9
	conda activate ray_torch
	conda install pytorch torchvision torchaudio pytorch-cuda=11.7 -c pytorch -c nvidia
	pip install pygame gymnasium opencv-python ray ray[rlib] ray[tune] dm-tree pandas scipy lz4
	
## Inference
You can do inference on a PC by adding your network checkpoint to the `ray_checkpoints` and modifying the `checkpoint_path` inside the `rayInferenceSnake.py` file.

## Run game
If you simply want to play the snake game with `WASD`, run `playSnake.py`. `R` for reset, `T` to kill the game.
