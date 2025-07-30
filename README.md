# 🗺️ Natural Language Route Planner

An agentic AI travel planner that interprets natural language instructions to generate dynamic, constraint-aware routes using NLP and OpenRouteService.

## 🚀 Features
- Parse natural language travel instructions
- Geocode places using `geopy`
- Generate driving routes via OpenRouteService API
- Apply constraints like avoiding highways or toll roads
- Modular, agent-based architecture

## 📦 Setup

```bash
git clone https://github.com/YOUR_USERNAME/natural-language-route-planner.git
cd natural-language-route-planner
pip install -r requirements.txt
export ORS_API_KEY=your_openrouteservice_api_key
python run.py
