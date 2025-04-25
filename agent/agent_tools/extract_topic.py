import json

from langchain_core.language_models import BaseLanguageModel

from agent.state import WorkflowState
from agent.prompts import extract_topic_prompt


def extract_topic(model: BaseLanguageModel):
    def extract_topic(state: WorkflowState):
        messages = extract_topic_prompt.invoke({"question": state["question"]})
        res = model.invoke(messages).content

        res = json.loads(res)["result"]

        return {"topic": res}

    return extract_topic
