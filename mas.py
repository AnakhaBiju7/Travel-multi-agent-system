import os, datetime, time
from groq import Groq
from utils import call_llm
from memory import setup_goal, load_goal, load_memory, save_memory
from search import search_agent
from agents import create_agents, opinion_agent, critic_agent, final_synthesizer

# ======================
# API KEYS
# ======================
GROQ_API_KEY = "key"
HOTEL_API_KEY = "key"
os.environ["GROQ_API_KEY"] = GROQ_API_KEY
os.environ["HOTEL_API_KEY"] = HOTEL_API_KEY

# ======================
# INIT CLIENT
# ======================
client = Groq(api_key=GROQ_API_KEY)
CHECK_INTERVAL = 10

# ======================
# AUTONOMOUS LOOP
# ======================
def autonomous_loop():
    while True:
        goal = load_goal()
        memory = load_memory()

        print("\n🔁 Checking at", datetime.datetime.now())
        hotels = search_agent(goal["city"], memory, HOTEL_API_KEY)
        if not hotels:
            print("No hotels found. Retrying in 60s...")
            time.sleep(60)
            continue

        # Price drop detection
        for hotel in hotels:
            name = hotel["name"]
            current_price = hotel["price"]
            previous_price = memory["last_prices"].get(name)
            if previous_price:
                drop = ((previous_price - current_price) / previous_price) * 100
                if drop >= goal["price_drop_alert_percent"]:
                    print(f"🚨 PRICE DROP for {name}! {round(drop,2)}%")

        # Multi-agent decisions
        agents = create_agents(client)
        opinions = [opinion_agent(client, agent, hotels, goal["budget"]) for agent in agents]
        critic = critic_agent(client, opinions)
        final = final_synthesizer(client, opinions, critic)

        print("🏆 Final Best Hotel:", final)

        # Update memory
        for hotel in hotels:
            memory["last_prices"][hotel["name"]] = hotel["price"]
        memory["decisions"].append({
            "time": str(datetime.datetime.now()),
            "decision": final
        })
        save_memory(memory)

        if not goal["monitor"]:
            print("Monitoring disabled. Exiting.")
            break

        print(f"Sleeping for {CHECK_INTERVAL}s...\n")
        time.sleep(CHECK_INTERVAL)

# ======================
# MAIN EXECUTION
# ======================
if __name__ == "__main__":
    print("🚀 Welcome to Level-4 Autonomous AI MAS Travel Planner")
    setup_goal()
    autonomous_loop()
