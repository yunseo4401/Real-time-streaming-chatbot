from flask import Flask, render_template, request, jsonify
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Message {self.content}>'

# Function to delete the existing database file
def delete_database_file():
    try:
        os.remove('messages.db')
        print("Deleted existing database file 'messages.db'")
    except FileNotFoundError:
        pass

@app.route("/")
def index():
    return render_template('index_making.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    content = data.get('content')
    timestamp_str = data.get('timestamp')
    timestamp = datetime.strptime(timestamp_str, '%I:%M %p | %B %d')
    message = Message(content=content, timestamp=timestamp)
    db.session.add(message)
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/messages')
def get_messages():
    messages = Message.query.all()
    messages_list = [{'content': msg.content, 'timestamp': msg.timestamp.strftime('%I:%M %p | %B %d')} for msg in messages]
    return jsonify(messages_list)

if __name__ == '__main__':
    with app.app_context():
        delete_database_file()  # Delete existing database file if it exists
        db.create_all()
    app.run(debug=True)
