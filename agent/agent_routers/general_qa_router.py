from agent.state import WorkflowState


def general_qa_router(state: WorkflowState):
    if state["topic"] == "other":
        return "generate_general_answer"
    return "generate_qa_answer"