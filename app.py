#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#/////////////////////////////////////////

# 🠺 07/04/2022 10:50:02
#
# ↳ Author 🡢 Mikołaj Połonowicz @ MCCXVI
# ↳ https://github.com/mccxvi/Pokemon-Crowd-Control-Flask/

#/////////////////////////////////////////

# Load modules to use
from flask import Flask, render_template, Response, request, redirect, url_for, flash, session, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, Regexp, ValidationError
from flask_bcrypt import Bcrypt
from pynput.keyboard import Listener, KeyCode, Key, Controller as KeyboardController
import time
import sys
import logging
import string
import random

# List holding users already playing / logged in
already_logged_in = []

# Turning off logging of http requests etc.
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

# Set pynput keyboard controller
keyboard = KeyboardController()

# Creating game code function
def keygen(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# Find playing user function
def search_user(list, platform):
    for i in range(len(list)):
        if list[i] == platform:
            return True
    return False

# Showing active game code in console
gamekey = keygen()
print(f"Key for the current game is: {gamekey}")

# Loading Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Login user input
class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=12)], render_kw={"placeholder": "Username"})
    authkey = StringField(validators=[InputRequired(), Length(min=6, max=6)], render_kw={"placeholder": "Game Key"})

    submit = SubmitField("Play")

# Login form page
@app.route('/auth', methods=['POST', 'GET'])
def authsesh():
    
    form = LoginForm()

    if form.validate_on_submit():
        user = request.form['username']
        if search_user(already_logged_in, user):
            return redirect(url_for('authsesh'))
        else:
            if gamekey == request.form['authkey']:
                session['user'] = request.form['username']
                already_logged_in.append(user)
                return redirect(url_for('game'))

    if session.get('user') is not None:
        return redirect(url_for('game'))

    return render_template("auth.html", form=form)

# Main game page
@app.route("/", methods=['POST', 'GET'])
def game():
    if session.get('user') is None:
        return redirect(url_for('authsesh'))
    else:
        return render_template('index.html', user=session['user'])

    return render_template('index.html', user=session['user'])

# Update page
# On users button press HTTP POST requests goes here, gets processed by pynput
# as a keyboard input and tells ajax to stay on the same site (just refresh on update)
@app.route("/update", methods=['POST', 'GET'])
def update():
    try:
        if session.get('user') is None:
            return redirect(url_for('game'))
        else:
            button_value = request.form['button_value']
            playing_user = session['user']
            print(f"{session['user']} pressed '{button_value}' Button")
            flash(f"You Have Pressed '{button_value}'")

            if button_value == "Up":
                up_button = Key.up
                keyboard.press(up_button)
                time.sleep(0.2)
                keyboard.release(up_button)
            elif button_value == "Down":
                down_button = Key.down
                keyboard.press(down_button)
                time.sleep(0.2)
                keyboard.release(down_button)
            elif button_value == "Left":
                left_button = Key.left
                keyboard.press(left_button)
                time.sleep(0.2)
                keyboard.release(left_button)
            elif button_value == "Right":
                right_button = Key.right
                keyboard.press(right_button)
                time.sleep(0.2)
                keyboard.release(right_button)
            elif button_value == "A":
                a_button = Key.backspace
                keyboard.press(a_button)
                time.sleep(0.1)
                keyboard.release(a_button)
            elif button_value == "B":
                b_button = Key.space
                keyboard.press(b_button)
                time.sleep(0.1)
                keyboard.release(b_button)
            elif button_value == "Start":
                start_button = Key.home
                keyboard.press(start_button)
                time.sleep(0.1)
                keyboard.release(start_button)
            elif button_value == "Select":
                select_button = Key.delete
                keyboard.press(select_button)
                time.sleep(0.1)
                keyboard.release(select_button)

            return jsonify({'result' : 'success'})
        
    except:
        return redirect(url_for('game'))

# Run flask web app
if __name__ == "__main__":
    app.run(debug=True, host="YOUR_IP")
