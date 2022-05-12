from flask import Flask, render_template, Response, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt
from pynput.keyboard import Listener, KeyCode, Key, Controller as KeyboardController
import time
import logging

# Turn off logging POST/GET messages in terminal
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

keyboard = KeyboardController()

# Defining Keys

up_button = Key.up
down_button = Key.down
left_button = Key.left
right_button = Key.right
a_button = Key.backspace
b_button = Key.space
start_button = Key.home
select_button = Key.delete

# App Flask Config
app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Login Session Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "authsesh"

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

# Models for authentication
class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12))
    authkey = db.Column(db.String(80))

class AddUsers(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=12)], render_kw={"placeholder": "Username"})
    authkey = PasswordField(validators=[InputRequired(), Length(min=8, max=32)], render_kw={"placeholder": "Auth Key"})

    submit = SubmitField("Add User")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=12)], render_kw={"placeholder": "Username"})
    authkey = PasswordField(validators=[InputRequired(), Length(min=8, max=32)], render_kw={"placeholder": "Auth Key"})

    submit = SubmitField("Login")

# Register Page
@app.route('/addusers', methods=['POST', 'GET'])
@login_required
def addusers():
#    if session['user'] != "YOUR_ADMIN_NAME":
#        return redirect("https://www.youtube.com/watch?v=ixMHG0DIAK4", code=302)
#    else:
    form = AddUsers()
    if form.validate_on_submit():
        hashed_authkey = bcrypt.generate_password_hash(form.authkey.data)
        new_user = users(username=form.username.data, authkey=hashed_authkey)
        db.session.add(new_user)
        db.session.commit()

    return render_template("addusers.html", form=form)

# Login Page
@app.route('/auth', methods=['POST', 'GET'])
def authsesh():
    if current_user.is_authenticated:
        return redirect(url_for('game'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = users.query.filter_by(username=form.username.data).first()
            if user:
                    if bcrypt.check_password_hash(user.authkey, form.authkey.data):
                        login_user(user)
                        session['user'] = request.form['username']
                        return redirect(url_for('game'))

    return render_template("auth.html", form=form)

# Main Game
@app.route("/", methods=['POST', 'GET'])
@login_required
def game():
    return render_template('index.html', user=session['user'])

# AJAX Post for movement update and pressing buttons
@app.route("/update", methods=['POST', 'GET'])
@login_required
def update():
    button_value = request.form['button_value']

    print(f"{session['user']} pressed '{button_value}' Button")
    flash(f"You Have Pressed '{button_value}'")

    if button_value == "Up":
        keyboard.press(up_button)
        time.sleep(0.3)
        keyboard.release(up_button)
    elif button_value == "Down":
        keyboard.press(down_button)
        time.sleep(0.3)
        keyboard.release(down_button)
    elif button_value == "Left":
        keyboard.press(left_button)
        time.sleep(0.3)
        keyboard.release(left_button)
    elif button_value == "Right":
        keyboard.press(right_button)
        time.sleep(0.3)
        keyboard.release(right_button)
    elif button_value == "A":
        keyboard.press(a_button)
        time.sleep(0.1)
        keyboard.release(a_button)
    elif button_value == "B":
        keyboard.press(b_button)
        time.sleep(0.1)
        keyboard.release(b_button)
    elif button_value == "Start":
        keyboard.press(start_button)
        time.sleep(0.1)
        keyboard.release(start_button)
    elif button_value == "Select":
        keyboard.press(select_button)
        time.sleep(0.1)
        keyboard.release(select_button)

    return jsonify({'result' : 'success'})

# Run Server
if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, host="YOUR_IP")