import json
from utils import safe_json_loads, call_llm

def create_agents(client):
    system_prompt = "You are an agent creator. Define 3 hotel selection agents with unique priorities. Respond ONLY with JSON."
    user_prompt = """
Return JSON array:
[
  {"name": "...", "rules": "..."}
]
Only JSON.
"""
    return safe_json_loads(call_llm(client, system_prompt, user_prompt))

def opinion_agent(client, agent, hotels, budget=None):
    system_prompt = f"You are {agent['name']}. Follow these rules: {agent['rules']}"
    user_prompt = f"""
Hotels:
{json.dumps(hotels, indent=2)}

Pick the best hotel under budget {budget} if possible.

Return ONLY JSON:
{{
 "selected_hotel": "...",
 "reason": "..."
}}
"""
    return safe_json_loads(call_llm(client, system_prompt, user_prompt))

def critic_agent(client, opinions):
    system_prompt = "You are a critic agent. Evaluate which agent selected the hotel best aligned with budget, rating, and value."
    user_prompt = f"""
Opinions:
{json.dumps(opinions, indent=2)}

Return ONLY JSON:
{{
 "best_opinion": "...",
 "critique": "..."
}}
"""
    return safe_json_loads(call_llm(client, system_prompt, user_prompt))

def final_synthesizer(client, opinions, critic_feedback):
    system_prompt = "You are a synthesizer agent. Combine agent opinions and critic feedback to select the final hotel."
    user_prompt = f"""
Agent Opinions:
{json.dumps(opinions, indent=2)}

Critic Feedback:
{json.dumps(critic_feedback, indent=2)}

Return ONLY JSON:
{{
 "final_selected_hotel": "...",
 "reason": "..."
}}
"""
    return safe_json_loads(call_llm(client, system_prompt, user_prompt))
