

from flask import Flask, render_template, url_for, flash, redirect, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import os # for our secret key

# APP INITIALIZATION

app = Flask(__name__)

app.config['SECRET_KEY'] = "This-is_secret-key"

# INITIALIZE FLASK-SOCKETIO

socketio = SocketIO(app, cors_allowed_origins="*")

#ROUTES
@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        #ACCEPT USER NAME
        name = request.form.get("name")
        room = request.form.get("room")

        if not name:
            flash("Enter a name to join chat", "danger")
            return render_template("index.html")
        
        #STORE THE NAME AND ROOM IN SESSION VARIABLE
        session["name"] = name
        session["room"] = room

        return redirect(url_for('chat'))
    #IF GET METHOD
    return render_template("index.html")

#CHATROOM
@app.route('/chat')
def chat():
    if 'name' not in session or 'room' not in session:
        flash('Please enter a name room to access the chat.', 'danger')
        return redirect(url_for('index'))
    
    #ELSE ENTER THE CHATROOM
    return render_template('chat.html', name = session['name'],room = session['room'])

#SOCKETIO EVENT HANDLERS
@socketio.on('join')
def on_join(data):
    name = data['name']
    room = data['room']
    join_room(room)
    emit('status', {'msg': f'{name} has entered the room. Say Hello!!', 'type':'info'},to = room)
    #LOG IT ON THE SERVER SIDE FOR DEBUGGING
    print(f'{name} has joined the : {room}')

@socketio.on('leave')
def on_leave(data):
    name = data['name']
    room = data['room']
    leave_room(room)
    emit('status', {'msg': f'{name} has left the room. Bye Bye', 'type':'wrong'}, to = room)
    print(f'{name} has left room: {room}')

@socketio.on('message')
def on_message(data):
    name = data['name']
    message = data['message']
    room = data['room']
    timestamp = data['timestamp']

    print(f"[{timestamp}] {name} in room {room}: {message}") #SERVER SIDE LOGGING
    emit("chat_message", {"name": name, "message": message, "timestamp": timestamp}, to = room )

@app.errorhandler(404)
def page_not_found(e):
    flash("Oops! That page does not exist. let's get you back to the chat.", "danger")
    return redirect(url_for('index'))

#RUNNING THE APP

if __name__=="__main__":
    socketio.run(app, debug=True)