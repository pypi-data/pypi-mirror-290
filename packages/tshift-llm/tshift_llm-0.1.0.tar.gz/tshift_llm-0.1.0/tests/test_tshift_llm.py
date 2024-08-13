import unittest
from unittest.mock import Mock, patch
from tshift_llm import tShift_LLM, LiteLLMClient

class TestTShiftLLM(unittest.TestCase):
    def setUp(self):
        self.mock_client1 = Mock(spec=LiteLLMClient)
        self.mock_client1.model = "openai/llama-3.1-405b-reasoning"
        self.mock_client2 = Mock(spec=LiteLLMClient)
        self.mock_client2.model = "openai/gpt-4o"
        self.tshift_llm = tShift_LLM([self.mock_client1, self.mock_client2])

    def test_completion_success(self):
        self.mock_client1.completion.return_value = "Success"
        result = self.tshift_llm.completion([{"role": "user", "content": "Test"}])
        self.assertEqual(result, "Success")

    def test_completion_fallback(self):
        self.mock_client1.completion.side_effect = Exception("Error")
        self.mock_client2.completion.return_value = "Fallback Success"
        result = self.tshift_llm.completion([{"role": "user", "content": "Test"}])
        self.assertEqual(result, "Fallback Success")

if __name__ == '__main__':
    unittest.main()
