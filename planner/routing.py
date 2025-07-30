import os
import requests

def planner_agent(coords, options):
    ORS_API_KEY = os.getenv("ORS_API_KEY")
    if not ORS_API_KEY:
        return {"error": "Missing ORS_API_KEY in environment variables."}
    if not coords or len(coords) < 2:
        return {"error": "Insufficient coordinates."}

    def call_api(coords_subset):
        url = "https://api.openrouteservice.org/v2/directions/driving-car"
        body = {
            "coordinates": coords_subset,
            "instructions": True,
            "options": {"avoid_features": options.get("avoid_features", [])}
        }
        headers = {
            "Authorization": ORS_API_KEY,
            "Content-Type": "application/json"
        }
        response = requests.post(url, json=body, headers=headers)
        return response

    # Try full route
    res = call_api(coords)
    if res.status_code == 200:
        return res.json()

    # Fallback: try with just origin and destination
    fallback_coords = [coords[0], coords[-1]]
    print("⚠️ Fallback: retrying with origin and destination only.")
    res = call_api(fallback_coords)
    if res.status_code == 200:
        return res.json()

    return {"error": "Route planning failed completely.", "status": res.status_code}
