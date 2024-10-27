from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

class WebsiteScraperRequest(Model):
    url: str


class WebsiteScraperResponse(Model):
    text: str


agent = Agent(
    name="scraper",
    mailbox="584f8b1d-a886-41e2-84e3-d56fdd15e169"
)

fund_agent_if_low(agent.wallet.address())

AI_AGENT_ADDRESS = "agent1qwnjmzwwdq9rjs30y3qw988htrvte6lk2xaak9xg4kz0fsdz0t9ws4mwsgs"

website_url = "https://resources.redcross.org/search_results/29002?widget=redcrossdisasterresources"

@agent.on_event("startup")
async def send_message(ctx: Context):
    await ctx.send(AI_AGENT_ADDRESS, WebsiteScraperRequest(url=website_url))
    ctx.logger.info(f"Request sent from -> {agent.address}")
    ctx.logger.info(f"Sent request for scraping the Website: {website_url}")


@agent.on_message(WebsiteScraperResponse)
async def handle_response(ctx: Context, sender: str, msg: WebsiteScraperResponse):
    ctx.logger.info(f"Received response from {sender[-10:]}:")
    ctx.logger.info(msg.text)


if __name__ == "__main__":
    agent.run()