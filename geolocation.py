from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low


class GeolocationRequest(Model):
    address: str


class GeolocationResponse(Model):
    latitude: float
    longitude: float


AGENT_MAILBOX_KEY = "818fd4d3-6def-49a1-aa36-4b70f1259db6"

agent = Agent(
    name="geolocation",
    seed="geolocationtesttesttest",
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
    port=8100
)

fund_agent_if_low(agent.wallet.address())


AI_AGENT_ADDRESS = "agent1qvnpu46exfw4jazkhwxdqpq48kcdg0u0ak3mz36yg93ej06xntklsxcwplc"


address = "Kings Cross Station, London"


@agent.on_event("startup")
async def send_message(ctx: Context):
    await ctx.send(AI_AGENT_ADDRESS, GeolocationRequest(address=address))
    ctx.logger.info(f"Sent address to Geolocation agent: {address}")


@agent.on_message(GeolocationResponse)
async def handle_response(ctx: Context, sender: str, msg: GeolocationResponse):
    ctx.logger.info(f"Received response from {sender}:")
    ctx.logger.info(f"Latitude: {msg.latitude}, Longitude: {msg.longitude}")

print(f"Agent address: {agent.wallet.address()}")

if __name__ == "__main__":
    agent.run()