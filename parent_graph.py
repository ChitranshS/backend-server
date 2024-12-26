from platform import node
from langgraph.graph import END, StateGraph, START
from state import ReWOO
from init_node import node as init_node
from dotenv import load_dotenv
from utils.checkpointer import checkpointer
from chat_node import node as chat_node
from langgraph.checkpoint.memory import MemorySaver
from termcolor import colored
from langchain_core.messages import HumanMessage, AIMessage
from other_node import node as other_node



# Add nodes
graph = StateGraph(ReWOO)
graph.add_node("init_node", init_node)
graph.add_node("chat", chat_node)
graph.add_node("a_prime", other_node)


# Add edges
graph.add_edge(START, "init_node")
graph.add_edge("init_node" , "chat")

graph.add_conditional_edges(
    "chat",
    lambda x: {
        False: END,
        True: ["a_prime"]
    }[x["task_ready"]]
)


graph.add_edge("a_prime", END)

# checkpointer = MemorySaver()


graph_runner = graph.compile(checkpointer=checkpointer)

async def run_agent(query,thread_id_provider):
     # memory = MemorySaver()
    config = {
            "configurable": {
            "thread_id": thread_id_provider
        }
    }

    formatted_query = query
    message_history = []
    message_history.append(HumanMessage(content=formatted_query))
    try:
            initial_state = ReWOO(messages=message_history , thread_id=thread_id_provider)
          
            for event in graph_runner.stream(initial_state, config=config):
                if isinstance(event, dict):
                    print(colored(event, "cyan"))
                    for node_name, node_value in event.items():

                        if node_name == "chat":
                             if isinstance(node_value, dict):
                                messages = node_value['messages']
                                # for message in messages:
                                if isinstance(messages[-1], AIMessage):
                                        print(colored(messages[-1].content, "red"))
                                        yield (messages[-1])
                        elif node_name == "other_node":
                            if isinstance(node_value, dict):
                                hotel_determined = node_value['hotel_determined']
                                intent = node_value['intent']
                                # for message in messages:
                                yield (AIMessage(content=f"Hotel Determined: {hotel_determined} , Intent: {intent} , Moving to existing workflow"))
                        

                               

    finally:
            print("Graph Execution Completed")



from langchain_core.runnables.graph import CurveStyle, MermaidDrawMethod, NodeStyles
import os

# Generate the Mermaid PNG
png_data = graph_runner.get_graph().draw_mermaid_png(
    draw_method=MermaidDrawMethod.API,
)

# Save the PNG data to a file
output_path = "graph_visualization.png"
with open(output_path, "wb") as f:
    f.write(png_data)

print(f"Graph visualization saved to: {os.path.abspath(output_path)}")