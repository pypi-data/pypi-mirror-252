import unittest

from dotenv import load_dotenv
from llama_index import (
    ServiceContext,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.vector_stores.types import BasePydanticVectorStore, VectorStore
from parameterized import parameterized
from unstract.sdk.tool.base import UnstractAbstractTool
from unstract.sdk.vector_db import UnstractToolVectorDB

load_dotenv(dotenv_path="backend/.env")


class ToolVectorDBTest(unittest.TestCase):
    class MockTool(UnstractAbstractTool):
        def run(
            self,
        ) -> None:
            self.stream_log("Mock tool running")

    def setUp(self) -> None:
        self.tool = self.MockTool()
        self.documents = SimpleDirectoryReader(
            "sdks/tests/samples/paul"
        ).load_data()

    @parameterized.expand(
        [
            [
                "d38a31be-3302-4017-8ae8-74209dfd5df7"
            ],  # Qdrant vector store (works)
            [
                "3dce2a4b-bc5b-4004-97c0-d48aca1a1a58"
            ],  # Postgres vector store (works)
        ]
    )
    def test_get_vector_db(self, adapter_instance_id: str) -> None:
        unstract_tool_vector_db = UnstractToolVectorDB(tool=self.tool)
        vector_store = unstract_tool_vector_db.get_vector_db(
            adapter_instance_id
        )
        self.assertIsNotNone(vector_store)
        self.assertIsInstance(
            vector_store, (BasePydanticVectorStore, VectorStore)
        )

        service_context = ServiceContext.from_defaults()
        storage_context = StorageContext.from_defaults(
            vector_store=vector_store
        )
        index = VectorStoreIndex.from_documents(
            self.documents,
            storage_context=storage_context,
            service_context=service_context,
        )
        query_engine = index.as_query_engine()

        response = query_engine.query("What did the author learn?")
        self.assertIsNotNone(response)


if __name__ == "__main__":
    unittest.main()
