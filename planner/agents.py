import time
import re
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from transformers import pipeline

llm = pipeline("text-generation", model="tiiuae/falcon-rw-1b")

def instruction_parser(instruction: str) -> dict:
    prompt = f"""
You are a route planning agent. Extract the following structured dictionary from the user instruction:
- origin (string)
- destination (string)
- waypoints (list of strings)
- constraints (dictionary with optional keys like "avoid")
Return ONLY the dictionary.
Instruction: "{instruction}"
"""
    output = llm(prompt, max_new_tokens=150, do_sample=False)[0]['generated_text']
    match = re.search(r"\{.*\}", output, re.DOTALL)
    if match:
        try:
            return eval(match.group(0))
        except:
            return {"error": "Parsing failed."}
    return {"error": "No dictionary found."}

def constraint_agent(constraints: dict) -> dict:
    prompt = f"""
You are a constraint translator for a routing system. Given this dictionary:
{constraints}
Convert it to a new dictionary with routing keys like:
- "avoid_features": list (e.g. ["tollways", "highways"])
Return only the new dictionary.
"""
    output = llm(prompt, max_new_tokens=100, do_sample=False)[0]['generated_text']
    match = re.search(r"\{.*\}", output, re.DOTALL)
    if match:
        try:
            return eval(match.group(0))
        except:
            return {"avoid_features": []}
    return {"avoid_features": []}

class GeocodeAgent:
    def __init__(self):
        self.locator = Nominatim(user_agent="route_planner_agent")

    def geocode(self, place: str):
        try:
            location = self.locator.geocode(place, timeout=10)
            if location:
                return (location.latitude, location.longitude)
        except GeocoderTimedOut:
            time.sleep(1)
            return self.geocode(place)
        return None