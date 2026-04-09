# main.py
# Entry point for the PolicyPilot AI Agent pipeline

from module2_classifier import classify_and_route

def main():
    print("=" * 50)
    print("  PolicyPilot — AI Bank Operations Agent")
    print("=" * 50)
    print("Type a request and the agent will classify and route it.")
    print("Type 'quit' to exit.\n")

    while True:
        user_input = input("Request: ").strip()

        if not user_input:
            continue

        if user_input.lower() == "quit":
            print("Goodbye!")
            break

        classify_and_route(user_input)
        print()


if __name__ == "__main__":
    main()