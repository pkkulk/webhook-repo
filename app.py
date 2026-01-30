from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import datetime
from dateutil import parser

app = Flask(__name__)

# MongoDB Setup
try:
    client = MongoClient('mongodb://localhost:27017/')
    db = client.webhook_db
    events_collection = db.events
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/events')
def get_events():
    # Fetch latest 10 events, sorted by timestamp descending
    events = list(events_collection.find({}, {'_id': 0}).sort('timestamp', -1).limit(10))
    return jsonify(events)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"msg": "No data received"}), 400

    event_type = request.headers.get('X-GitHub-Event')
    
    # Common fields
    record = {
        "timestamp_obj": datetime.datetime.utcnow(), 
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

    # Handle Push Event
    if event_type == 'push':
        record['type'] = 'PUSH'
        record['author'] = data.get('pusher', {}).get('name', 'Unknown')
        record['to_branch'] = data.get('ref', '').split('/')[-1]
        
        # Adjust format: "Travis" pushed to "staging" on 1st April 2021 - 9:30 PM UTC
        # We will format on the frontend or backend. 
        # Requirement says:
        # Format: {author} pushed to {to_branch} on {timestamp}
        # Sample: "Travis" pushed to "staging" on 1st April 2021 - 9:30 PM UTC
        
    # Handle Pull Request Event
    elif event_type == 'pull_request':
        action = data.get('action')
        pr_data = data.get('pull_request', {})
        
        if action == 'closed' and pr_data.get('merged'):
            record['type'] = 'MERGE'
            record['author'] = pr_data.get('merged_by', {}).get('login', 'Unknown')
            record['from_branch'] = pr_data.get('head', {}).get('ref', 'Unknown')
            record['to_branch'] = pr_data.get('base', {}).get('ref', 'Unknown')
        elif action in ['opened', 'reopened']:
            record['type'] = 'PULL_REQUEST'
            record['author'] = pr_data.get('user', {}).get('login', 'Unknown')
            record['from_branch'] = pr_data.get('head', {}).get('ref', 'Unknown')
            record['to_branch'] = pr_data.get('base', {}).get('ref', 'Unknown')
        else:
            return jsonify({"msg": "Ignored PR action"}), 200

    else:
        return jsonify({"msg": "Ignored event type"}), 200

    # Store in DB
    events_collection.insert_one(record)
    return jsonify({"msg": "Event received"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
