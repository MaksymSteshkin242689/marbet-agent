import json

from langchain_core.language_models import BaseLanguageModel

from agent.state import WorkflowState
from agent.prompts import generate_general_answer_prompt


def generate_general_answer(model: BaseLanguageModel):
    def generate_general_answer(state: WorkflowState):
        prompt = generate_general_answer_prompt.invoke({"question": state["question"]})
        res = model.invoke(prompt).content

        res = json.loads(res)["answer"]

        return {"answer": res}

    return generate_general_answer
