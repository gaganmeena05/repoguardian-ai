from pathlib import Path

from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from config import settings

PERSIST_DIR = settings.vector_store_path

# Configure embedding model
Settings.embed_model = HuggingFaceEmbedding(
    model_name=settings.embedding_model
)


class RepositoryRAG:
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.index = None

    def build_index(self):
        """
        Build a new index from the repository.
        """

        documents = SimpleDirectoryReader(
            input_dir=str(self.repo_path),
            recursive=True,
            exclude=[
                ".git",
                ".github",
                ".venv",
                "__pycache__",
                "node_modules",
                ".vector_store",
                "dist",
                "build",
            ],
        ).load_data()

        self.index = VectorStoreIndex.from_documents(
            documents,
            show_progress=True,
        )

        self.index.storage_context.persist(
            persist_dir=PERSIST_DIR,
        )

        return self.index

    def load_index(self):
        """
        Load an existing persisted index.
        """

        storage_context = StorageContext.from_defaults(
            persist_dir=PERSIST_DIR,
        )

        self.index = load_index_from_storage(
            storage_context,
        )

        return self.index

    def get_index(self):
        """
        Return an index, building it if necessary.
        """

        if self.index is not None:
            return self.index

        if Path(PERSIST_DIR).exists():
            return self.load_index()

        return self.build_index()

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
    ) -> str:
        """
        Retrieve relevant repository context.
        """

        index = self.get_index()

        query_engine = index.as_query_engine(
            similarity_top_k=top_k,
        )

        response = query_engine.query(query)

        return str(response)

    def rebuild(self):
        """
        Force rebuilding the vector index.
        """

        if Path(PERSIST_DIR).exists():
            import shutil

            shutil.rmtree(PERSIST_DIR)

        return self.build_index()