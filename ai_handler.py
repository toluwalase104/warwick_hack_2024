from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low

class TextPrompt(Model):
    text: str


class TextResponse(Model):
    text: str

def run_query(recipient_information: list[tuple[int, str, str]], donor_information: list[tuple[int, str, str]]):
    # Define agent name and mailbox (offline storage area)
    agent = Agent(
        name="claude-handler",
        mailbox="1d104283-0bba-401d-abdb-221c671399f4"
    )

    fund_agent_if_low(agent.wallet.address())

    # Address of the claude ai being used under the hood
    AI_AGENT_ADDRESS = "agent1qvk7q2av3e2y5gf5s90nfzkc8a48q3wdqeevwrtgqfdl0k78rspd6f2l4dx"

    prompts = [
        f"Benefactor - I need {required_resources}. Additionally: {extra_information}\n\
            {[f"Donor {id} offers {resources}. Additionally {extra}" for id, resources, extra in donor_information]}\n\
            List the donors in order of who best matches the benefactor, with no additional information."
        for _, required_resources, extra_information in recipient_information   
    ]

    # for prompt in prompts:
    #     print(prompts)
    # prompts = [
    #     f"Benefactor - I need {required_resources}. Additionally: {extra_information}\n\
    #         {donor_information}\n\
    #         Sort the donors in order of who best matches the benefactor.",       
    # ]

    # When the fetch agent starts up it sends a prompt
    @agent.on_event("startup")
    async def send_message(ctx: Context):
        for prompt in prompts:
            await ctx.send(AI_AGENT_ADDRESS, TextPrompt(text=prompt))
            ctx.logger.info(f"Sending from agent address:{agent.address}")
            ctx.logger.info(f"[Sent prompt to AI agent]: {prompt}")

    # Outputs the message received from the offline agent
    @agent.on_message(TextResponse)
    async def handle_response(ctx: Context, sender: str, msg: TextResponse):
        ctx.logger.info(f"[Received response from ...{sender[-8:]}]:")
        ctx.logger.info(msg.text)

    agent.run()
    """
    """


if __name__ == "__main__":
    requests1 = ["transport", "food", "money"]
    requests2 = ["food", "shelter"]

    extra_details = "I have a family of four" 

    provisions = ["Donor A - offers transport, for at most 8 passengers. \
                    Donor B - offers food, for at most 5 people.\
                        Donor C - offers food and shelter. \
                            Donor D - offers money, donating up to $1000\
                        Sort the donors in order of who best matches the benefactor."
                  ]
    
    run_query(requests1, extra_details, provisions)
    # agent.run()