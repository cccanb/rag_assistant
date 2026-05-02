from functools import lru_cache
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pathlib import Path
from ..constants.constants import INDEX_DIR, EMBEDDING_MODEL, GPT_MODEL


@lru_cache(maxsize=1)
def _load_vectorstore() -> FAISS:
    return FAISS.load_local(
        folder_path=str(Path(INDEX_DIR)),
        embeddings=OpenAIEmbeddings(model=EMBEDDING_MODEL),
        allow_dangerous_deserialization=True,
    )


class QAService:
    NUMBER_OF_DOCS = 5

    PROMPT_TEMPLATE = PromptTemplate(
        input_variables=["context", "question"],
        template="""
            You are an assistant answering questions based on documentation.
            Use only the information from the context below. If the answer is not explicitly stated, respond with "I don't know."

            Context:
            {context}

            Question:
            {question}

            Answer:
        """
    )

    def __init__(self):
        self.vectorstore = _load_vectorstore()

    def get_answer(self, query: str) -> str:
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": self.NUMBER_OF_DOCS})

        qa = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(model=GPT_MODEL, temperature=0),
            retriever=retriever,
            chain_type="stuff",
            chain_type_kwargs={"prompt": self.PROMPT_TEMPLATE}
        )

        response = qa.invoke({"query": query})
        return response.get("result", response)
