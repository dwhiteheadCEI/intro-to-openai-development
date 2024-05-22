import os
import random
from openai import OpenAI
from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField

# To use the completed version of this app, please copy and paste this file overtop of the 'app.py' 
# file in the lab6 folder in the base 'lab-files' directory.

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

client = OpenAI(api_key="")
socketio = SocketIO(app)

def generate_image(input):
    styleInfo = open("static/example-prompts/image-generation.txt").read()
    input = styleInfo + input

    response = client.images.generate(
        model="dall-e-3",
        prompt=input,
        size="1792x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url

def generate_response(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.75,
    )
    return response.choices[0].message.content

#
# Web app code below
#

class SetupForm(FlaskForm):
    crime = TextAreaField('Describe the crime')
    suspect1 = StringField('Name') 
    suspect2 = StringField('Name') 
    suspect3 = StringField('Name')
    suspect1Desc = TextAreaField('Description') 
    suspect2Desc = TextAreaField('Description') 
    suspect3Desc = TextAreaField('Description')
    
    submit = SubmitField('>')

@app.route('/')
def welcome():
    return render_template('welcome.html')
    
@app.route('/setup', methods=['GET', 'POST'])
def setup():
    form = SetupForm()
    if request.method == 'GET':
        # Setting up our default values
        form.crime.data = open("static/example-prompts/offense.txt").read()
        form.suspect1.data = "Claudia Hargrove"
        form.suspect1Desc.data = open("static/example-prompts/suspect1.txt").read()
        form.suspect2.data = "Margaret Marsh"
        form.suspect2Desc.data = open("static/example-prompts/suspect2.txt").read()
        form.suspect3.data = "Vincent Hargrove"
        form.suspect3Desc.data = open("static/example-prompts/suspect3.txt").read()
    if form.validate_on_submit():
        # Process form data
        evilNum = random.randrange(1, 4, 1)
        suspects = [
            {
                'name': form.suspect1.data,
                'description': form.suspect1Desc.data,
                'image': generate_image(form.suspect1Desc.data),
                'guilty': True if evilNum == 1 else False
            },
            {
                'name': form.suspect2.data,
                'description': form.suspect2Desc.data,
                'image': generate_image(form.suspect2Desc.data),
                'guilty': True if evilNum == 2 else False
            },
            {
                'name': form.suspect3.data,
                'description': form.suspect3Desc.data,
                'image': generate_image(form.suspect3Desc.data),
                'guilty': True if evilNum == 3 else False
            }
        ]
        session['evilNum'] = evilNum
        session['suspects'] = suspects
        session['chat_history'] = {1: [], 2: [], 3: []}  # Initialize chat history for each suspect
        return redirect(url_for('game'))
    
    return render_template('setup.html', form=form)

@app.route('/game')
def game():
    suspects = session.get('suspects', [])
    return render_template('game.html', suspects=suspects)

@app.route('/results', methods=['POST'])
def results():
    choice = int(request.form['choice'])
    evilNum = session.get('evilNum')  # Assuming evilNum is stored in the session
    didIWin = choice == evilNum
    return render_template('results.html', victory=didIWin)

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    message = data['message']
    suspect_index = int(data['suspect'])
    suspects = session.get('suspects', [])
    chat_history = {int(k): v for k, v in session.get('chat_history', {1: [], 2: [], 3: []}).items()}

    if not suspects:
        return jsonify({'error': 'No suspects found in session'}), 400

    suspect = suspects[suspect_index - 1]

    # Update chat history
    chat_history[suspect_index].append({"role": "user", "content": "user: " + message})

    # Define our messages to send to the bot
    role_message = {"role": "system", "content": open("static/example-prompts/role.txt").read()}
    persona_message = {"role": "system", "content": f"Suspect description: {suspect['description']}."}
    guilty_message = {"role": "system", "content": f"Guilty status: {suspect['guilty']}"}
    messages = [role_message, persona_message, guilty_message] + chat_history[suspect_index]

    # Generate response
    response_text = generate_response(messages)
    
    # Update chat history with the suspect's response
    chat_history[suspect_index].append({"role": "assistant", "content": response_text})
    session['chat_history'] = chat_history

    return jsonify({'response': response_text})

@socketio.on('message')
def handle_message(data):
    emit('response', {'data': data['data'], 'suspect': data['suspect']}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
