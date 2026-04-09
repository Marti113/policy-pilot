# module3_integrations.py

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("TRELLO_API_KEY")
TOKEN = os.getenv("TRELLO_TOKEN")
BOARD_ID = os.getenv("TRELLO_BOARD_ID")


def get_todo_list_id():
    """Get the ID of the 'To Do' list on the board."""
    url = f"https://api.trello.com/1/boards/{BOARD_ID}/lists"
    params = {"key": API_KEY, "token": TOKEN}
    response = requests.get(url, params=params)
    lists = response.json()
    for lst in lists:
        if "to do" in lst["name"].lower():
            return lst["id"]
    # If no 'To Do' list, just use the first one
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


if __name__ == "__main__":
    result = create_trello_card("Review the Henderson account by Friday")
    print(f"Card created: {result['name']}")
    print(f"URL: {result['url']}")