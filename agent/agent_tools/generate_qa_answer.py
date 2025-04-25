import json

from langchain_core.language_models import BaseLanguageModel

from agent.context_store import ContextStore
from agent.state import WorkflowState
from agent.prompts import generate_qa_answer_prompt


def generate_qa_answer(model: BaseLanguageModel, extract_store):
    def generate_qa_answer(state: WorkflowState):
        store: ContextStore = extract_store(state["topic"])
        docs = store.get_context()

        prompt = generate_qa_answer_prompt.invoke({"question": state["question"], "context": docs})
        res = model.invoke(prompt).content

        res = json.loads(res)["answer"]

        return {"answer": res}

    return generate_qa_answer