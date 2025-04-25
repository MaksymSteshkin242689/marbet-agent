from langchain_community.document_loaders import TextLoader


class ContextStore:
    def __init__(self):
        self.docs = None

    def load_context(self, path):
        loader = TextLoader(file_path=path)
        docs = loader.load()

        self.docs = docs

    def get_context(self):
        return self.docs