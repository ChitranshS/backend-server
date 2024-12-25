from termcolor import colored
from chat_wrapper import stream_graph_updates
import uuid
def node(state):
    print(colored("---Chat Node---", "light_blue"))
    updated_state = stream_graph_updates(state=state)
    if "inner_messages" in updated_state:
        state['messages'] = updated_state['inner_messages']
        print(colored(state['messages'][-1].content,"yellow"))
    elif "should_end" in updated_state and updated_state['should_end']:
        state['task_ready'] = True
        state['hotel_determined'] = updated_state['hotel_determined']
        state['intent'] = updated_state['intent']
    return state