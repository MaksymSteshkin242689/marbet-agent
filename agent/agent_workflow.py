from langchain_core.language_models import BaseLanguageModel

from agent.agent_routers.general_qa_router import general_qa_router
from agent.agent_tools.extract_topic import extract_topic
from agent.agent_tools.generate_general_answer import generate_general_answer
from agent.agent_tools.generate_qa_answer import generate_qa_answer
from agent.context_store import ContextStore
from agent.state import WorkflowState


class AgentWorkflow:
    def __init__(self, model: BaseLanguageModel):
        self.stores = AgentWorkflow.__load_stores()
        self.model = model

        self.graph = self.__build_graph()

    def start_flow(self, question: str):
        return self.graph.invoke({"question": question})["answer"]

    def __build_graph(self):
        from langgraph.graph import START, StateGraph, END

        graph_builder = StateGraph(WorkflowState)

        graph_builder.add_node(extract_topic(self.model), "extract_topic")
        graph_builder.add_node(generate_general_answer(self.model), "generate_general_answer")
        graph_builder.add_node(generate_qa_answer(self.model, self.__extract_store_from_topic), "generate_qa_answer")

        graph_builder.add_edge(START, "extract_topic")

        graph_builder.add_conditional_edges("extract_topic", general_qa_router)

        graph_builder.add_edge("generate_general_answer", END)
        graph_builder.add_edge("generate_qa_answer", END)

        return graph_builder.compile()

    def __extract_store_from_topic(self, topic):
        return self.stores[topic]

    @staticmethod
    def __load_stores():
        activities_store = ContextStore()
        company_store = ContextStore()
        esta_store = ContextStore()
        eta_store = ContextStore()
        packlist_store = ContextStore()
        a_to_z_store = ContextStore()
        spa_store = ContextStore()
        wifi_store = ContextStore()

        activities_store.load_context(path="splitted/activities.txt")
        company_store.load_context(path="splitted/company.txt")
        esta_store.load_context(path="splitted/esta.txt")
        eta_store.load_context(path="splitted/eta.txt")
        packlist_store.load_context(path="splitted/packlist.txt")
        a_to_z_store.load_context(path="splitted/scenic-eclipse-a-z")
        spa_store.load_context(path="splitted/spa.txt")
        wifi_store.load_context(path="splitted/wifi.txt")

        return {
            "activities": activities_store,
            "company": company_store,
            "esta": esta_store,
            "eta": eta_store,
            "packlist": packlist_store,
            "scenic-eclipse-a-z": a_to_z_store,
            "spa": spa_store,
            "wifi": wifi_store
        }
