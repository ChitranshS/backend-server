from typing import List
from typing_extensions import TypedDict
from langgraph.graph import MessagesState


class ReWOO(MessagesState):
    task_ready: bool
    result: str
    should_end : bool
    thread_id: str
    