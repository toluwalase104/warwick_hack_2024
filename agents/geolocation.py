from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
import asyncio


class GeolocationRequest(Model):
    address: str


class GeolocationResponse(Model):
    latitude: float
    longitude: float

address = "Kings Cross Station, London"


def run_geolocation_agent(address):

    AGENT_MAILBOX_KEY = "818fd4d3-6def-49a1-aa36-4b70f1259db6"

    agent = Agent(
        name="geolocation",
        seed="geolocationtesttesttest",
        mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
        port=8100
    )

    fund_agent_if_low(agent.wallet.address())

    print("Funded agent") # TEST

    AI_AGENT_ADDRESS = "agent1qvnpu46exfw4jazkhwxdqpq48kcdg0u0ak3mz36yg93ej06xntklsxcwplc"


    @agent.on_event("startup")
    async def send_message(ctx: Context):
        await ctx.send(AI_AGENT_ADDRESS, GeolocationRequest(address=address))
        ctx.logger.info(f"Sent address to Geolocation agent: {address}")


    @agent.on_message(GeolocationResponse)
    async def handle_response(ctx: Context, sender: str, msg: GeolocationResponse):
        ctx.logger.info(f"Received response from {sender}:")
        ctx.logger.info(f"Latitude: {msg.latitude}, Longitude: {msg.longitude}")
        with open("geolocation.txt", "w") as f:
            f.write(f"{msg.latitude},{msg.longitude}")
            # the first one is latitude and the second one is longitude
        raise ValueError("Test error to stop agent")
    
    agent.run()


# run_geolocation_agent(address) # Uncomment this line to test the agent locally