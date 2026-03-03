from fastapi import APIRouter
from database import jet_collection, airport_collection
from utils.helpers import calculate_distance

router = APIRouter(tags=["Recommendations"])


@router.get("/recommend")
async def recommend(departure: str, arrival: str, passengers: int, budget: float):
    """
    Recommend a jet based on departure/arrival airports, passenger count, and budget.
    Budget is in millions (e.g. 50 = $50M).
    """
    budget = budget * 1000000

    jets = await jet_collection.find().to_list(length=None)
    airports = await airport_collection.find().to_list(length=None)

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
                    "estimated_cost": round(total_cost, 0),
                    "image_url": jet.get("image_url", "/images/def-jet.png"),
                })

    if not possible_jets:
        return {"message": "No jet fits this budget and route"}

    possible_jets.sort(key=lambda x: x["estimated_cost"])

    return possible_jets[0]
