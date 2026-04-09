# module3_integrations.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Trello
API_KEY = os.getenv("TRELLO_API_KEY")
TOKEN = os.getenv("TRELLO_TOKEN")
BOARD_ID = os.getenv("TRELLO_BOARD_ID")

# Slack
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

# ServiceNow
SNOW_INSTANCE = os.getenv("SNOW_INSTANCE")
SNOW_USERNAME = os.getenv("SNOW_USERNAME")
SNOW_PASSWORD = os.getenv("SNOW_PASSWORD")


def get_todo_list_id():
    """Get the ID of the 'To Do' list on the board."""
    url = f"https://api.trello.com/1/boards/{BOARD_ID}/lists"
    params = {"key": API_KEY, "token": TOKEN}
    response = requests.get(url, params=params)
    lists = response.json()
    for lst in lists:
        if "to do" in lst["name"].lower():
            return lst["id"]
    return lists[0]["id"]


def create_trello_card(task_description: str) -> dict:
    """Create a card in the To Do list on the PolicyPilot board."""
    list_id = get_todo_list_id()

    url = "https://api.trello.com/1/cards"
    params = {
        "key": API_KEY,
        "token": TOKEN,
        "idList": list_id,
        "name": task_description,
        "desc": "Created automatically by PolicyPilot AI Agent"
    }

    response = requests.post(url, params=params)
    card = response.json()

    return {
        "id": card["id"],
        "name": card["name"],
        "url": card["shortUrl"]
    }


def send_slack_notification(message: str) -> dict:
    """Send a notification message to the PolicyPilot Slack channel."""
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": SLACK_CHANNEL_ID,
        "text": f"🤖 PolicyPilot Alert:\n{message}"
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()

    return {
        "ok": result["ok"],
        "channel": result.get("channel"),
        "message": message
    }


def create_servicenow_incident(description: str) -> dict:
    """Create an incident ticket in ServiceNow."""
    url = f"https://{SNOW_INSTANCE}/api/now/table/incident"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "short_description": description,
        "description": "Created automatically by PolicyPilot AI Agent",
        "category": "inquiry",
        "urgency": "3",
        "impact": "3"
    }

    response = requests.post(
        url,
        auth=(SNOW_USERNAME, SNOW_PASSWORD),
        headers=headers,
        json=payload
    )
    result = response.json().get("result", {})

    return {
        "number": result.get("number"),
        "sys_id": result.get("sys_id"),
        "url": f"https://{SNOW_INSTANCE}/nav_to.do?uri=incident.do?sys_id={result.get('sys_id')}",
        "description": description
    }


if __name__ == "__main__":
    # Test Trello
    card = create_trello_card("Review the Henderson account by Friday")
    print(f"Trello card created: {card['name']}")
    print(f"URL: {card['url']}")

    # Test Slack
    slack = send_slack_notification("Test alert from PolicyPilot")
    print(f"Slack message sent: {slack['ok']}")

    # Test ServiceNow
    incident = create_servicenow_incident("Review Henderson account for compliance flags")
    print(f"ServiceNow incident created: {incident['number']}")
    print(f"URL: {incident['url']}")
    # Debug ServiceNow
    url = f"https://{SNOW_INSTANCE}/api/now/table/incident"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "short_description": "Test incident from PolicyPilot",
        "category": "inquiry",
        "urgency": "3",
        "impact": "3"
    }
    response = requests.post(
        url,
        auth=(SNOW_USERNAME, SNOW_PASSWORD),
        headers=headers,
        json=payload
    )
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")