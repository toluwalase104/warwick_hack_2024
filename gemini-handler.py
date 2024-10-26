from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

class Prompt(Model):
    text: str

class Response(Model):
    text: str


agent = Agent(
    name="gemini-handler",
    mailbox="f7daec4e-dc3e-4c40-980f-b404cee37d75"
)

fund_agent_if_low(agent.wallet.address())

AI_AGENT_ADDRESS = "agent1qt70gnyr355uhlrxk68ralyhq2tx9xqj0d6a07r4twvvrtjgrmzjkgpgvq2"

prompts = [
    "Benefactor - I need transport, food, shelter. Additionally: I have a family of four\
        Donor A - offers transport, for at most 8 passengers. Donor B - offers food, for at most 5 people.\
              Donor C - offers food and shelter. Donor D - offers money, donating up to $1000\
            Sort the donors in order of who best matches the benefactor.",
    "Benefactor - I need money, food, shelter.\
        Donor A - offers transport, for at most 8 passengers. Donor B - offers food, for at most 5 people.\
              Donor C - offers food and shelter. Donor D - offers money, donating up to $1000\
            Sort the donors in order of who best matches the benefactor.",            
]

@agent.on_event("startup")
async def send_message(ctx: Context):
    for prompt in prompts:
        await ctx.send(
            AI_AGENT_ADDRESS,
            Prompt(
                text=prompt,
            ),
        )
        ctx.logger.info(f"Prompt sent from address - {agent.address}")
        ctx.logger.info(f"Sent prompt to AI agent: {prompt}")


@agent.on_message(Response)
async def handle_response(ctx: Context, sender: str, msg: Response):
    ctx.logger.info(f"Received response from {sender}:")
    ctx.logger.info(msg.text)


if __name__ == "__main__":
    agent.run()
