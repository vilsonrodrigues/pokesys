from langgraph.graph import StateGraph
from langgraph_supervisor import create_supervisor
from pokesys.agents.expert import expert_agent
from pokesys.agents.generation.schemas import SupervisorResponse
from pokesys.agents.prompts.supervisor import SUPERVISOR_SYSTEM_PROMPT
from pokesys.agents.researcher import researcher_agent
from pokesys.agents.tools.supervisor import SUPERVISOR_TOOLS
from pokesys.llm import get_llm


def build_graph() -> StateGraph:
    """
    Build and return the agent workflow graph.
    
    Returns:
        Compiled Graph
    """
    workflow = create_supervisor(
        agents=[researcher_agent, expert_agent],
        model=get_llm(),
        prompt=SUPERVISOR_SYSTEM_PROMPT,
        #tools=SUPERVISOR_TOOLS,
        response_format=SupervisorResponse,
    )
    workflow.compile()
    return workflow

graph = build_graph()
