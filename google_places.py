from typing import Any, Dict, List, Optional
from uagents.setup import fund_agent_if_low
from uagents import Model, Agent, Context
import asyncio

class Coordinates(Model):
    latitude: float
    longitude: float

class POIAreaRequest(Model):
    loc_search: Coordinates
    radius_in_m: int
    limit: int = 20
    query_string: str
    filter: Dict[str, Any] = {}

class POI(Model):
    placekey: str
    location_name: str
    brands: Optional[List[str]] = None
    top_category: Optional[str] = None
    sub_category: Optional[str] = None
    location: Coordinates
    address: str
    city: str
    region: Optional[str] = None
    postal_code: str
    iso_country_code: str
    metadata: Optional[Dict[str, Any]] = None

class POIResponse(Model):
    loc_search: Coordinates
    radius_in_m: int
    data_origin: str
    data: List[POI]



def run_google_places_agent(latitude, longitude, item):

    query = "shelter"
    if item == "medicine":
        query = "first aid"
    elif item == "water":
        query = "water refill station near me"
    elif item == "food":
        query = "food bank"
    elif item == "clothes":
        query = "free clothing bank"

    AGENT_MAILBOX_KEY = "eff0bf6a-39db-4e64-bba8-a0ae522ddc3e"
    SEED_PHRASE = "sadasdasfjhasodfhpubsndvy2wq"

    # Initialize the agent
    agent = Agent(
        name="google_places",
        seed=SEED_PHRASE,
        mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
    )

    fund_agent_if_low(agent.wallet.address())

    GMAPS_AGENT_ADDRESS = "agent1qvcqsyxsq7fpy9z2r0quvng5xnhhwn3vy7tmn5v0zwr4nlm7hcqrckcny9e"

    coords = Coordinates(latitude=latitude, longitude=longitude)

    example_request = POIAreaRequest(
        loc_search=coords,
        radius_in_m=2000,
        query_string=f"{query}",  # Modify based on the type of help needed
    )


    @agent.on_event("startup")
    async def handle_startup(ctx: Context):
        await ctx.send(GMAPS_AGENT_ADDRESS, example_request)
        ctx.logger.info(f"Sent request to Google Maps agent: {example_request}")


    @agent.on_message(POIResponse)
    async def handle_response(ctx: Context, sender: str, msg: POIResponse):
        ctx.logger.info(f"Received {len(msg.data)} POIs from: {sender}")
        if len(msg.data) > 0:
            print(f"Received {len(msg.data)} POIs")
            # Write the received POIs to google_places.txt
            with open("google_places.txt", "w") as f:
                for place in msg.data:
                    lat = place.location.latitude
                    lon = place.location.longitude
                    f.write(f"{place.location_name}\t{lat}\t{lon}\n")
                    print(f"Wrote {place.location_name} at ({lat}, {lon}) to google_places.txt")
        else:
            print("No POIs found")
            with open("google_places.txt", "w") as f:
                f.write("")
            print("Wrote 'No POIs found' to google_places.txt")

    agent.run()

# run_google_places_agent(52.4084048,-1.510218, "shelter") # Uncomment this line to test the agent locally
