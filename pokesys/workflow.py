import json
from pokesys.graph.builder import graph


async def run_workflow_async(question: str):
    """Run the agent workflow asynchronously with the given user input.

    Args:
        question: The user's query.
    
    Returns:
        The final state after the workflow completes.
    """
    if not question:
        raise ValueError("Input could not be empty")

    output = await graph.ainvoke({"messages": [{"role": "user", "content": question}]})
    response = json.loads(output["messages"][-1].content)
    return response    
