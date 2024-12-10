# File: server/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
CORS(app) 

@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.order_by(Message.created_at).all()
    return jsonify([message.to_dict() for message in messages])

@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    body = data.get('body')
    username = data.get('username')
    if not body or not username:
        return jsonify({"error": "Invalid input"}), 400

    message = Message(body=body, username=username)
    db.session.add(message)
    db.session.commit()
    return jsonify(message.to_dict()), 201

@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    data = request.get_json()
    message = Message.query.get_or_404(id)
    if 'body' in data:
        message.body = data['body']
    db.session.commit()
    return jsonify(message.to_dict())

@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    return jsonify({"message": "Message deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=4000)
