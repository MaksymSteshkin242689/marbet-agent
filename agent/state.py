from typing_extensions import TypedDict


class WorkflowState(TypedDict):
    question: str
    topic: str
    answer: str