import folium
from planner.agents import instruction_parser, GeocodeAgent, constraint_agent
from planner.routing import planner_agent

def run():
    user_input = input("Enter your travel instruction: ")

    print("\n [Agent 1] Parsing instruction")
    parsed = instruction_parser(user_input)
    if "error" in parsed:
        print("Parse error:", parsed["error"])
        return
    print("Parsed:", parsed)

    print("\n [Agent 2] Geocoding locations")
    geo = GeocodeAgent()
    origin = geo.geocode(parsed["origin"])
    destination = geo.geocode(parsed["destination"])
    waypoints = [geo.geocode(w) for w in parsed.get("waypoints", []) if geo.geocode(w)]

    if not origin or not destination:
        print("Geocoding failed for key locations.")
        return

    print("\n [Agent 3] Processing constraints...")
    routing_options = constraint_agent(parsed.get("constraints", {}))
    print("Routing Options:", routing_options)

    coords = [origin] + waypoints + [destination]
    print("\n [Agent 4] Planning route...")
    route = planner_agent(coords, routing_options)

    if "error" in route:
        print("Route Error:", route)
        return
    
    print("Route Success! Previewing static map")

    m = folium.Map(location=origin, zoom_start=7)
    folium.Marker(origin, tooltip='Origin', icon=folium.Icon(color='green')).add_to(m)
    for idx, wp in enumerate(waypoints):
        folium.Marker(wp, tooltip=f'Waypoint {idx+1}').add_to(m)
    folium.Marker(destination, tooltip='Destination', icon=folium.Icon(color='red')).add_to(m)

    try:
        coords_list = route['features'][0]['geometry']['coordinates']
        coords_latlon = [(lat, lon) for lon, lat in coords_list]
        folium.PolyLine(coords_latlon, color='blue').add_to(m)
    except:
        print("Route drawn only with markers (geometry unavailable).")

    m.save("route_map.html")
    print("Map saved as route_map.html — open it in a browser.")
