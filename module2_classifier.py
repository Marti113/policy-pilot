# module2_classifier.py

import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

# --- Tool definitions (what Claude can choose from) ---
tools = [
    {
        "name": "classify_request",
        "description": "Classify an incoming bank operations request into the correct category so it can be routed appropriately.",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "enum": ["policy_question", "create_task", "send_notification", "trigger_workflow", "unknown"],
                    "description": "The category that best fits the request."
                },
                "reasoning": {
                    "type": "string",
                    "description": "Brief explanation of why this category was chosen."
                }
            },
            "required": ["category", "reasoning"]
        }
    }
]

# --- Router: calls the right handler based on category ---
def route_request(category, original_request):
    if category == "policy_question":
        print("  → Routing to RAG pipeline (module1)...")
        from module1_rag import ask_policy_question
        answer = ask_policy_question(original_request)
        print(f"  RAG Answer: {answer}")

    elif category == "create_task":
        print("  → Would create a Trello task (module3 - coming soon)")
        print(f"  Task: {original_request}")

    elif category == "send_notification":
        print("  → Would send a notification (module3 - coming soon)")
        print(f"  Message: {original_request}")

    elif category == "trigger_workflow":
        print("  → Would trigger n8n workflow (module3 - coming soon)")
        print(f"  Workflow trigger: {original_request}")

    else:
        print("  → Unknown request type. Logging and skipping.")
        print(f"  Unhandled: {original_request}")


# --- Main classifier function ---
def classify_and_route(request: str):
    print(f"\nIncoming request: '{request}'")
    print("Classifying...")

    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        tools=tools,
        messages=[
            {
                "role": "user",
                "content": f"""You are an AI agent for a bank operations team. 
Classify this incoming request into the correct category and explain your reasoning.

Request: {request}"""
            }
        ]
    )

    # Extract the tool use block
    for block in response.content:
        if block.type == "tool_use" and block.name == "classify_request":
            category = block.input["category"]
            reasoning = block.input["reasoning"]
            print(f"  Category: {category}")
            print(f"  Reasoning: {reasoning}")
            route_request(category, request)
            return category

    print("  Claude did not use the classification tool.")
    return "unknown"


# --- Test it ---
if __name__ == "__main__":
    test_requests = [
        "What is the maximum LTV ratio allowed for jumbo loans?",
        "Create a task to review the Henderson account by Friday",
        "Send a notification to the compliance team about the new audit",
        "Trigger the end-of-day reconciliation workflow",
        "gjkahsdgkjashd",  # unknown/garbage
    ]

    for req in test_requests:
        classify_and_route(req)
        print()