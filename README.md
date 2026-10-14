# CSE423 Labs — Computer Graphics

Four interactive Python/OpenGL exercises: a raining house, bouncing balls, a diamond-catching game, and a 3D shooting game. Each script opens its own GLUT window and keeps the drawing, animation, and input handling in one file.

## Pick an exercise

| Script | What it explores |
| --- | --- |
| [Raining House Motion.py](Raining%20House%20Motion.py) | A house scene with animated rain |
| [Ball Game.py](Ball%20Game.py) | Moving balls and mouse/keyboard interaction |
| [DiamondCatcher.py](DiamondCatcher.py) | Catching falling diamonds with midpoint-line drawing |
| [3D Shooting Game.py](3D%20Shooting%20Game.py) | A 3D player, enemies, projectiles, and camera controls |

## Run locally

Use Python 3, PyOpenGL, and a working native OpenGL/GLU/GLUT runtime. A desktop display is required. Installing the Python package alone may not supply your operating system's GLUT library.

```bash
python -m pip install PyOpenGL
python "DiamondCatcher.py"
```

Replace the filename to launch another exercise:

```bash
python "Raining House Motion.py"
python "Ball Game.py"
python "3D Shooting Game.py"
```

If a GLUT function cannot be loaded, check that a compatible native GLUT/freeglut library is installed and available to the Python process.

## Controls

The input callbacks in each file are the source of truth for its controls.

- **Diamond Catcher:** left/right arrows move the catcher; Space pauses, R restarts, and Escape exits.
- **Ball Game:** mouse buttons interact with the balls; Space toggles the freeze state, and up/down arrows change speed.
- **3D Shooting Game:** W/S move, A/D rotate, left-click fires, right-click changes camera mode, and the arrow keys adjust the camera. C toggles cheat mode; R resets the game.

## About this collection

These are standalone graphics coursework exercises. There is no shared launcher or pinned environment, and behavior depends on local graphics support. The interactive programs have not been run as part of this documentation update.
