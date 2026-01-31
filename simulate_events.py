import requests
import time
import json

URL = "http://localhost:5000/webhook"

def send_push():
    print("Sending PUSH event...")
    headers = {'X-GitHub-Event': 'push', 'Content-Type': 'application/json'}
    data = {
        "ref": "refs/heads/staging",
        "pusher": {"name": "Prathmesh"}
    }
    try:
        response = requests.post(URL, json=data, headers=headers)
        if response.status_code == 200:
             print(f"Status: {response.status_code}, Response: {response.json()}")
        else:
             print(f"Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Failed to send PUSH: {e}")

def send_pr_open():
    print("Sending PR OPEN event...")
    headers = {'X-GitHub-Event': 'pull_request', 'Content-Type': 'application/json'}
    data = {
        "action": "opened",
        "pull_request": {
            "user": {"login": "Prathmesh"},
            "head": {"ref": "staging"},
            "base": {"ref": "master"},
            "merged": False
        }
    }
    try:
        response = requests.post(URL, json=data, headers=headers)
        if response.status_code == 200:
             print(f"Status: {response.status_code}, Response: {response.json()}")
        else:
             print(f"Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Failed to send PR: {e}")

def send_merge():
    print("Sending MERGE event...")
    headers = {'X-GitHub-Event': 'pull_request', 'Content-Type': 'application/json'}
    data = {
        "action": "closed",
        "pull_request": {
            "merged": True,
            "merged_by": {"login": "Prathmesh"},
            "head": {"ref": "dev"},
            "base": {"ref": "master"}
        }
    }
    try:
        response = requests.post(URL, json=data, headers=headers)
        if response.status_code == 200:
             print(f"Status: {response.status_code}, Response: {response.json()}")
        else:
             print(f"Status: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Failed to send MERGE: {e}")

if __name__ == "__main__":
    print("Starting simulation...")
    time.sleep(1) 
    
    send_push()
    time.sleep(2)
    send_pr_open()
    time.sleep(2)
    send_merge()
    print("Simulation complete.")
