import asyncio
import json
from database import jet_collection, airport_collection

async def seed_data():
    with open("data/jets.json") as f:
        jets = json.load(f)

    with open("data/airports.json") as f:
        airports = json.load(f)

    await jet_collection.delete_many({})
    await airport_collection.delete_many({})

    await jet_collection.insert_many(jets)
    await airport_collection.insert_many(airports)

    print("Data inserted successfully")

asyncio.run(seed_data())