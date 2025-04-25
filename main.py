from langchain_ollama import ChatOllama

from agent.agent_workflow import AgentWorkflow


def main():
    model = ChatOllama(
        base_url="http://194.171.191.226:3061",
        model="llama3.1:70b",
        format="json"
    )
    agent = AgentWorkflow(model=model)


    questions = [
        "Hi! How can I connect to wifi?",
        "I have a family with a kid of 3 years and my father is very old. Which activity will be the best for us?",
        "How can I get a visa to USA?",
        "Tell me about your company?",
        "Give me the price for a barber"
    ]
    while True:
        question = input("Question: ")

        res = agent.start_flow(question)
        print(res)

if __name__ == '__main__':
    main()