# Webhook Receiver

Flask application to receive GitHub Webhooks and store them in MongoDB.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run MongoDB:
   ```bash
   sudo systemctl start mongod
   ```
3. Run the application:
   ```bash
   python3 app.py
   ```

## Testing

Use the simulation script in `../action-repo/simulate_events.py` to send mock events.
