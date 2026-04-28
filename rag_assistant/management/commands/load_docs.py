from django.core.management.base import BaseCommand
from rag_assistant.services.embedding import MarkdownEmbedder
from ...constants.constants import INDEX_DIR, DOCS_DIR


class Command(BaseCommand):
    help = "Loads markdown documents and builds FAISS index."

    def handle(self, *args, **kwargs):
        docs_path = DOCS_DIR
        index_path = INDEX_DIR
        embedder = MarkdownEmbedder(docs_path, index_path)
        embedder.build_index()
