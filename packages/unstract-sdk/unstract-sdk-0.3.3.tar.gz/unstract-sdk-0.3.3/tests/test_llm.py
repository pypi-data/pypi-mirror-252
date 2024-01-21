import json
import os
import re
import unittest
from typing import Any

from dotenv import load_dotenv
from parameterized import parameterized
from unstract.sdk.llm import UnstractToolLLM
from unstract.sdk.tool.base import UnstractAbstractTool

load_dotenv()


def get_test_values(env_key: str) -> list[str]:
    test_values = json.loads(os.environ.get(env_key))
    return test_values


class ToolLLMTest(unittest.TestCase):
    class MockTool(UnstractAbstractTool):
        def run(
            self,
            params: dict[str, Any] = {},
            settings: dict[str, Any] = {},
            workflow_id: str = "",
        ) -> None:
            # self.stream_log("Mock tool running")
            pass

    @classmethod
    def setUpClass(cls):
        cls.tool = cls.MockTool()

    @parameterized.expand(
        get_test_values("LLM_TEST_VALUES")
        # AzureOpenAI (Works)
        # OpenAI (Works)
        # AnyScale (llm FAILS)
        # Anthropic (llm.complete FAILS)
        # 1. unsupported params: max_token, stop.
        # TypeError: create() got an unexpected keyword argument
        # 'max_tokens'
        # 2. anthropic.APIConnectionError: Connection error.
        # PaLM (Works)
        # Errors
        # 1. unexpected keyword argument 'max_tokens', 'stop'
        # Replicate (llm.complete FAILS)
        # Errors
        # 1. replicate.exceptions.ReplicateError:
        # You did not pass an authentication token
        # Mistral (llm.complete FAILS)
        # Errors
        # 1.TypeError: chat() got an unexpected keyword argument 'stop'
    )
    def test_get_llm(self, adapter_instance_id):
        tool_llm = UnstractToolLLM(tool=self.tool)
        llm = tool_llm.get_llm(adapter_instance_id)
        self.assertIsNotNone(llm)
        # Removed params max_tokens=50, stop=[".", "\n"]
        response = llm.complete(
            "The capital of Tamilnadu is ",
            temperature=0.003,
        )
        response_lower_case: str = response.text.lower()
        print(response_lower_case)
        find_match = re.search("chennai", response_lower_case)
        if find_match:
            result = True
        else:
            result = False
        self.assertTrue(result)


if __name__ == "__main__":
    unittest.main()
