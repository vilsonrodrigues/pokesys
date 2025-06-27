from langgraph.prebuilt import create_react_agent
from pokesys.agents.prompts.expert import EXPERT_SYSTEM_PROMPT
from pokesys.agents.tools.expert import EXPERT_TOOLS
from pokesys.llm import get_llm


expert_agent = create_react_agent(
    name="pokemon_expert",
    model=get_llm(),
    tools=EXPERT_TOOLS,
    prompt=EXPERT_SYSTEM_PROMPT
)
