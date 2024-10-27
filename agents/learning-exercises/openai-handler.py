from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

class ContextPrompt(Model):
    context: str
    text: str


class Response(Model):
    text: str


agent = Agent(
    name="openai-handler",
    mailbox="4cbe7a24-2ace-4777-afd6-2cb4ebda67b1"
)

fund_agent_if_low(agent.wallet.address())

AI_AGENT_ADDRESS = "agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y"

prompts = [
    "Benefactor - I need transport, food, shelter. Additionally: I have a family of four\
        Donor A - offers transport, for at most 8 passengers. Donor B - offers food, for at most 5 people.\
              Donor C - offers food and shelter. Donor D - offers money, donating up to $1000",
    "Benefactor - I need money, food, shelter.\
        Donor A - offers transport, for at most 8 passengers. Donor B - offers food, for at most 5 people.\
              Donor C - offers food and shelter. Donor D - offers money, donating up to $1000\
            Sort the donors in order of who best matches the benefactor.",            
]

prompt = ContextPrompt(
    context="Sort the donors in order of who best matches the benefactor.",
    text="Benefactor - I need money, food, shelter.\
            Donor A - offers transport, for at most 8 passengers.\
                Donor B - offers food, for at most 5 people.\
                    Donor C - offers food and shelter.\
                        Donor D - offers money, donating up to $1000."
)

@agent.on_event("startup")
async def send_message(ctx: Context):
    # for prompt in prompts:
    #     await ctx.send(AI_AGENT_ADDRESS, prompt)
    ctx.logger.info(f"Sending from agent address:{agent.address}")
    ctx.logger.info(f"[Sent prompt to AI agent]: {prompt}")
    await ctx.send(AI_AGENT_ADDRESS, prompt)

@agent.on_message(Response)
async def handle_response(ctx: Context, sender: str, msg: Response):
    ctx.logger.info(f"[Received response from ...{sender[-8:]}]:")
    ctx.logger.info(msg.text)


if __name__ == "__main__":
    agent.run()