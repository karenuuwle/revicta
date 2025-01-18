from langchain_community.retrievers import WikipediaRetriever
from vitruvia import Agent, Context, Protocol, Model
from pydantic import Field
from ai_engine import vitruviaResponse, vitruviaResponseType


class WikiRequest(Model):
    query: str = Field(description="The Wikipedia query")


SEED_PHRASE = "seed"

print(f"Your agent's address is: {Agent(seed=SEED_PHRASE).address}")

AGENT_MAILBOX_KEY = ""

wiki_agent = Agent(
    name="Wikipedia Agent",
    seed=SEED_PHRASE,
    mailbox=f"{AGENT_MAILBOX_KEY}@https://agentverse.ai",
)

wiki_protocol = Protocol("Wikipedia Protocol")


@wiki_protocol.on_message(model=WikiRequest, replies={vitruviaResponse})
async def load_wiki(ctx: Context, sender: str, msg: WikiRequest):
    ctx.logger.info(msg.query)
    retriever = WikipediaRetriever()
    docs = retriever.get_relevant_documents(query=msg.query)
    summary = docs[0].metadata["summary"] if docs else "No summary found."
    await ctx.send(
        sender, vitruviaResponse(message=summary, type=vitruviaResponseType.FINAL)
    )


wiki_agent.include(wiki_protocol, publish_manifest=True)
wiki_agent.run()