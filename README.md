# Pokémon Crowd Control Flask

Flask (Front/Back End) server that controls Pokémon game with specified keyboard inputs in real time.

![Demo](demo.gif)

If you are looking for Discord version of this script, go here: [Pokémon Crowd Control (Discord)](https://gitlab.com/MCCXVI/pokemon-crowd-control)


## Setup

Before cloning repo, make sure you are using Python 3.9 or newer.<br />
Python 2.7 is deprecated/obsolete by now and will not work with this project.

Clone repo and create virtual environment
```
git clone https://gitlab.com/MCCXVI/pokemon-crowd-control-flask.git
python3 -m venv pokemon-crowd-control-flask
cd pokemon-crowd-control-flask
```

Activate the virtual environment for this project

Windows /
```
Scripts\activate.bat
```

Linux & MacOS /

```
source bin/activate
```

Install required packages with pip

```
pip install -r requirements.txt
```

## Prep for the Flask App

Change the SECRET_KEY to something else. It should be confidential and never shared with anyone.
```
app.config['SECRET_KEY'] = 'SECRET_KEY'
```

Set "YOUR_IP" to your local IP Address.
```
app.run(debug=True, host="YOUR_IP")
```

Change keys for the pynput depending on binded keys in your GBA Emulator.

Here are all the attrebutes of pynput.keyboard.Key 
- 'alt', 'backspace', 'cmd', 'ctrl', 'delete', 'down', 'end', 'enter',
- 'esc', 'f1', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18',
- 'f19', 'f2', 'f20', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'home',
- 'insert','left', 'menu', 'pause', 'right', 'shift', 'space', 'tab', 'up'

```
# Defining Keys

up_button = Key.up
down_button = Key.down
left_button = Key.left
right_button = Key.right
a_button = Key.backspace
b_button = Key.space
start_button = Key.home
select_button = Key.delete
```

## Running App

Run "app.py" in your terminal 
```
python app.py
Key for the current game is: XXXXXX
```

Everytime the app starts, it will generate unique six-character key code for the game.


## Playing

Go to

```
YOUR_IP:5000/auth
```

Choose a nickname and enter the Game Key provided in the terminal.
