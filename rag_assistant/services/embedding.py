from langchain.text_splitter import MarkdownHeaderTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from pathlib import Path
from ..constants.constants import EMBEDDING_MODEL


class MarkdownEmbedder:
    def __init__(self, docs_path: str, index_path: str):
        self.docs_path = Path(docs_path)
        self.index_path = Path(index_path)
        self.splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[
            ("#", "h1"),
            ("##", "h2"),
            ("###", "h3")
        ])
        self.embedding_model = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    def load_documents(self):
        markdown_files = list(self.docs_path.glob("*.md"))
        documents = []
        for file in markdown_files:
            with open(file, encoding="utf-8") as f:
                content = f.read()
                docs = self.splitter.split_text(content)
                documents.extend(docs)
        return documents

    def build_index(self):
        documents = self.load_documents()

        vectorstore = FAISS.from_documents(documents, self.embedding_model)

        self.index_path.mkdir(parents=True, exist_ok=True)
        vectorstore.save_local(str(self.index_path))
