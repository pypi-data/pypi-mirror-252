import unittest

from dotenv import load_dotenv
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.embeddings.google_palm import GooglePaLMEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from unstract.sdk.embedding import UnstractToolEmbedding
from unstract.sdk.tool.base import UnstractAbstractTool

load_dotenv(dotenv_path="backend/.env")


class ToolEmbeddingTest(unittest.TestCase):
    class MockTool(UnstractAbstractTool):
        def run(
            self,
        ) -> None:
            self.stream_log("Mock tool running")

    def setUp(self) -> None:
        self.tool = self.MockTool()

    def run_embedding_test(
        self, adapter_instance_id, embedding_id, embedding_class, test_text
    ):
        embedding = UnstractToolEmbedding(tool=self.tool)
        embed_model = embedding.get_embedding(adapter_instance_id)
        print(f"\n{embedding_id} : ", embed_model)
        self.assertIsNotNone(embed_model)
        self.assertIsInstance(embed_model, embedding_class)
        response = embed_model._get_text_embedding(test_text)
        print(f"\nResponse {embedding_id} : ", response)
        self.assertIsNotNone(response)

    def test_get_embedding_azure_openai(self) -> None:
        self.run_embedding_test(
            "87451925-b38d-4e67-98aa-4e8a90e5bd95",
            "AzureOpenAI",
            AzureOpenAIEmbedding,
            "Text snippet for Azure Open AI",
        )

    def test_get_embedding_openai(self) -> None:
        self.run_embedding_test(
            "0d1453cf-33e5-4280-a0fc-ac1cb2774765",
            "OpenAI",
            OpenAIEmbedding,
            "This is a test for OpenAI",
        )

    def test_get_embedding_palm(self) -> None:
        self.run_embedding_test(
            "0a7c31a4-0b87-40c1-85bc-83858a5d839e",
            "PALM",
            GooglePaLMEmbedding,
            "This is a test for PALM",
        )


if __name__ == "__main__":
    unittest.main()
