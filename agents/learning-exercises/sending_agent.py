from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

class WebsiteScraperRequest(Model):
    url: str

class WebsiteScraperResponse(Model):
    text: str

AGENT_MAILBOX_KEY="14c15c80-4c3b-4594-9b3f-a116bad0a2fa"
agent = Agent(
    name="user",
     seed="sample-seed",
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
    
)

fund_agent_if_low(agent.wallet.address())

AI_AGENT_ADDRESS = "agent1qwnjmzwwdq9rjs30y3qw988htrvte6lk2xaak9xg4kz0fsdz0t9ws4mwsgs"

website_url = "https://resources.redcross.org/search_results/29002?widget=redcrossdisasterresources&ref=DCSclient"


@agent.on_event("startup")
async def send_message(ctx: Context):
    ctx.logger.info(agent.address)
    await ctx.send(AI_AGENT_ADDRESS, WebsiteScraperRequest(url=website_url))
    ctx.logger.info(f"Sent request for scraping the Website: {website_url}")


@agent.on_message(WebsiteScraperResponse)
async def handle_response(ctx: Context, sender: str, msg: WebsiteScraperResponse):
    ctx.logger.info(f"Received response from {sender[-10:]}:")
    ctx.logger.info("The message was " + msg.text)

    await ctx.send(AI_AGENT_ADDRESS, WebsiteScraperRequest(url=website_url))


if __name__ == "__main__":
    agent.run()