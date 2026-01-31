# Webhook Receiver Project

This is a Flask application that listens for GitHub Webhooks and displays the events on a real-time dashboard.

## Features
- **Receives Webhooks**: Listens for `push`, `pull_request`, and `merge` events from GitHub.
- **Data Storage**: Stores all event data in a MongoDB database (MongoDB Atlas).
- **Real-Time UI**: Displays the events in a clean list, updating automatically every 15 seconds.

## Prerequisites
Before you start, make sure you have:
1.  **Python 3.x** installed.
2.  **MongoDB Atlas URI** (connection string).

## Setup Instructions

### 1. Install Dependencies
Open your terminal in this folder and run:
```bash
pip install -r requirements.txt
```

### 2. Configure Database
Create a file named `.env` in this folder and add your MongoDB connection string:
```bash
MONGO_URI=your_mongodb_connection_string_here
```
*(Note: Never commit your `.env` file to GitHub!)*

### 3. Run the Application
Start the server by running:
```bash
python3 app.py
```
You should see output indicating the server is running on `http://127.0.0.1:5000`.

### 4. View the Dashboard
Open your web browser and go to:
**http://localhost:5000**

## Project Structure
- `app.py`: The main Python file containing the Flask server and logic.
- `templates/index.html`: The HTML file for the frontend user interface.
- `requirements.txt`: List of Python libraries needed to run the app.
- `simulate_events.py`: (Optional) Script to test the app if you don't have a live GitHub repo connected.
