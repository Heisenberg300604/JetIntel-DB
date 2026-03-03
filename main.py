from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import math

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("data/jets.json") as f:
    jets = json.load(f)

with open("data/airports.json") as f:
    airports = json.load(f)

# Haversine formula to calculate distance
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 3440  # nautical miles
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )

    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))

@app.get("/recommend")
def recommend(departure: str, arrival: str, passengers: int, budget: float):

    dep = next((a for a in airports if a["iata"] == departure.upper()), None)
    arr = next((a for a in airports if a["iata"] == arrival.upper()), None)

    if not dep or not arr:
        return {"error": "Invalid airport code"}

    distance = calculate_distance(dep["lat"], dep["lng"], arr["lat"], arr["lng"])

    possible_jets = []

    for jet in jets:
        if jet["range_nm"] >= distance and jet["max_passengers"] >= passengers:
            flight_time = distance / jet["cruise_knots"]
            total_cost = flight_time * jet["cost_per_hour"]

            if total_cost <= budget:
                possible_jets.append({
                    "jet": jet["model"],
                    "manufacturer": jet["manufacturer"],
                    "flight_time_hours": round(flight_time, 2),
                    "distance_nm": round(distance, 0),
                    "estimated_cost": round(total_cost, 0)
                })

    if not possible_jets:
        return {"message": "No jet fits this budget and route"}

    # Sort by cheapest
    possible_jets.sort(key=lambda x: x["estimated_cost"])

    return possible_jets[0]