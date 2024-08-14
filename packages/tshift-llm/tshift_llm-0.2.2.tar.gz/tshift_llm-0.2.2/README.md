# ThinkShift_LLM
ThinkShift_LLM is a flexible LLM manager that shifts between multiple language models to ensure robust and uninterrupted AI-powered conversations.

## Features

- Manages multiple LiteLLM clients
- Shifts between models when errors occur
- Supports both streaming and non-streaming completions
- Detailed logging of all interactions
- Round-robin client selection

## Installation

You can install tShift_LLM using pip:

```
pip install tshift-llm
```

## Usage

Here's a quick example of how to use tShift_LLM:

```python
from tshift_llm import tShift_LLM, LiteLLMClient

clients = [
    LiteLLMClient("gpt-3.5-turbo", "your-openai-key"),
    LiteLLMClient("claude-2", "your-anthropic-key"),
    LiteLLMClient("command-nightly", "your-cohere-key")
]

tshift_llm = tShift_LLM(clients)

response = tshift_llm.completion(
    messages=[{"role": "user", "content": "Hello, how are you?"}]
)
print(response.choices[0].message.content)
```

For more detailed usage instructions, please refer to the documentation.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
