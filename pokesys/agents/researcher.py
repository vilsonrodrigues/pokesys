from langgraph.prebuilt import create_react_agent
from pokesys.agents.prompts.researcher import RESEARCHER_SYSTEM_PROMPT
from pokesys.agents.tools.researcher import RESEARCHER_TOOLS
from pokesys.llm import get_llm


researcher_agent = create_react_agent(
    name="pokemon_researcher",
    model=get_llm(),
    tools=RESEARCHER_TOOLS,
    prompt=RESEARCHER_SYSTEM_PROMPT,
)
