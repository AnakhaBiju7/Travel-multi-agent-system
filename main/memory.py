import json

def setup_goal():
    city = input("Enter city: ")
    budget = int(input("Enter budget: "))
    monitor = input("Monitor continuously? (yes/no): ").lower() == "yes"
    drop_percent = int(input("Alert if price drops by %: "))

    goal = {
        "city": city,
        "budget": budget,
        "monitor": monitor,
        "price_drop_alert_percent": drop_percent
    }
    with open("goal.json", "w") as f:
        json.dump(goal, f, indent=2)
    print("✅ Goal saved!")

def load_goal():
    with open("goal.json", "r") as f:
        return json.load(f)

def load_memory():
    try:
        with open("memory.json", "r") as f:
            return json.load(f)
    except:
        return {"last_prices": {}, "decisions": []}

def save_memory(memory):
    with open("memory.json", "w") as f:
        json.dump(memory, f, indent=2)
