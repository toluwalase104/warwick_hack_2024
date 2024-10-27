from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
import time

class ContextPrompt(Model):
    context: str
    text: str

class TextPrompt(Model):
    text: str

class TextResponse(Model):
    text: str

class Response(Model):
    text: str

def run_query(ai_id: int, recipient_information: list[tuple[int, str, str]], donor_information: list[tuple[int, str, str]]):
    
    if ai_id == 0: # 0 is the identifier for Claude
        print("Working with Claude")
        # Define agent name and mailbox (offline storage area)
        agent = Agent(
            name="claude-handler",
            mailbox="1d104283-0bba-401d-abdb-221c671399f4"
        )

        # Address of the claude ai being used under the hood
        AI_AGENT_ADDRESS = "agent1qvk7q2av3e2y5gf5s90nfzkc8a48q3wdqeevwrtgqfdl0k78rspd6f2l4dx"

        prompts = [
            f"Benefactor - I need {required_resources}. Additionally: {extra_information}. {". ".join([f"Donor {id} offers {resources}. Additionally {extra}" for id, resources, extra in donor_information])}. List the ids of the donors in order of who best matches the benefactor, with no additional information."
            for _, required_resources, extra_information in recipient_information   
        ]
    # elif ai_id == 1: # 1 is the identifier for Gemini
    #     print("Working with Gemini")
    #     # Define agent name and mailbox (offline storage area)
    #     agent = Agent(
    #         name="gemini-handler",
    #         mailbox="f7daec4e-dc3e-4c40-980f-b404cee37d75"
    #     )

    #     # Address of the claude ai being used under the hood
    #     AI_AGENT_ADDRESS = "agent1qt70gnyr355uhlrxk68ralyhq2tx9xqj0d6a07r4twvvrtjgrmzjkgpgvq2"

    #     # Split prompts into context and text, for open-ai
    #     prompts = [
    #         f"Benefactor - I need {required_resources}. Additionally: {extra_information}. {". ".join([f"Donor {id} offers {resources}. Additionally {extra}" for id, resources, extra in donor_information])}. List the ids of the donors in order of who best matches the benefactor, with no additional information."
    #         for _, required_resources, extra_information in recipient_information   
    #     ]
    else: # 2 is the identifier for OpenAI
        print("Working with OpenAI")
        # Define agent name and mailbox (offline storage area)
        agent = Agent(
            name="openai-handler",
            mailbox="dc51a5d9-ce2a-460c-8be7-a26105a2a098"
        )


        # Address of the claude ai being used under the hood
        AI_AGENT_ADDRESS = "agent1q0h70caed8ax769shpemapzkyk65uscw4xwk6dc4t3emvp5jdcvqs9xs32y"

        # Split prompts into context and text, for open-ai
        prompts = [
            ("List the ids of the donors in order of who best matches the benefactor, with no additional information, in the format [best_donor_match, ..., worst_donor_match]",
             f"Benefactor - I need {required_resources}. Additionally: {extra_information}. {". ".join([f"Donor {id} offers {resources}. Additionally {extra}" for id, resources, extra in donor_information])}"
            )
            for _, required_resources, extra_information in recipient_information   
        ]

    for prompt in prompts:
        print(prompt)

    print(agent.address)

    fund_agent_if_low(agent.wallet.address())

    # When the fetch agent starts up it sends a prompt
    @agent.on_event("startup")
    async def send_message(ctx: Context):
        for prompt in prompts:
            formatted_prompt = TextPrompt(text=prompt) if ai_id == 0 else ContextPrompt(context=prompt[0], text=prompt[1])

            await ctx.send(AI_AGENT_ADDRESS, formatted_prompt)

            ctx.logger.info(f"Sending from agent address:{agent.address}")
            ctx.logger.info(f"[Sent prompt to AI agent]: {formatted_prompt}")

    if ai_id == 0:
        # Outputs the message received from the offline agent
        @agent.on_message(TextResponse)
        async def handle_response(ctx: Context, sender: str, msg: TextResponse):
            ctx.logger.info(f"[Received response from ...{sender[-8:]}]:")
            ctx.logger.info(msg.text)

            time.sleep(5)          
            # If there is no message generated don't write anything
            if len(msg.text) == 0: 
                return
            with open("response.txt", "a") as f:
                f.write(msg.text + "\n") 

    else:
        @agent.on_message(model = Response)
        async def handle_response(ctx: Context, sender: str, msg: Response):
            ctx.logger.info(f"[Received response from ...{sender[-8:]}]:")
            ctx.logger.info(msg.text)

            time.sleep(5)          
            # If there is no message generated don't write anything
            if len(msg.text) == 0: 
                return
            with open("response.txt", "a") as f:
                f.write(msg.text + "\n") 

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