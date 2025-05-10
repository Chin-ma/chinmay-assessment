from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import os

app = Flask(__name__)

# MongoDB 
client = MongoClient("mongodb+srv://chinmay:chini@cluster0.rqwcnte.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["reminder_app"]
reminders_collection = db["reminders"]

@app.route('/reminder', methods=['POST'])
def create_reminder():
    data = request.json

    date = data.get('date')      # 'YYYY-MM-DD'
    time = data.get('time')      # 'HH:MM'
    message = data.get('message')
    method = data.get('method')  # 'sms' or 'email'

    if not all([date, time, message, method]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        remind_at = datetime.strptime(f"{date} {time}", '%Y-%m-%d %H:%M')
    except ValueError:
        return jsonify({'error': 'Invalid date or time format'}), 400

    reminder_doc = {
        "message": message,
        "remind_at": remind_at,
        "method": method,
        "created_at": datetime.utcnow()
    }

    result = reminders_collection.insert_one(reminder_doc)

    return jsonify({
        'message': 'Reminder created successfully',
        'reminder_id': str(result.inserted_id)
    }), 201

if __name__ == '__main__':
    app.run(debug=True)


# To test the api endpoint:
# Use this is linux terminal:

# curl -X POST http://localhost:5000/reminder \
#      -H "Content-Type: application/json" \
#      -d '{
#            "date": "2025-05-11",
#            "time": "14:30",
#            "message": "Join the Zoom call",
#            "method": "email"
#          }'


# Steps to Test in Postman

# Open Postman
# Set Method: `POST`
# Enter URL: `http://localhost:5000/reminder`
# Go to the `Body` tab:

# Select `raw`
# Choose `JSON`
# Paste the JSON body:

# {
#   "date": "2025-05-11",
#   "time": "14:30",
#   "message": "Join the Zoom call",
#   "method": "email"
# }

# 6. Click `Send`



















