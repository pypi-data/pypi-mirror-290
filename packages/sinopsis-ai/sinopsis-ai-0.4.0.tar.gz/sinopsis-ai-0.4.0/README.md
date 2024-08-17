
<img src="https://i.imgur.com/fM3G71D.png" alt="Sinopsis AI Cover Image">

# Official Sinopsis AI SDK for Python

[![PyPI version](https://img.shields.io/pypi/v/sinopsis-ai.svg)](https://pypi.org/project/sinopsis-ai/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is the official Python SDK for interacting with [Sinopsis AI](https://www.sinopsisai.com), designed to simplify the process of logging user prompts and responses, and managing conversation data.

## Features

- **Easy Integration**: Quickly integrate Sinopsis AI into your Python applications.
- **Session Management**: Start, manage, and end sessions with ease.
- **Conversation Logging**: Log user prompts and assistant responses with timestamps.
- **API Interaction**: Communicate with the Sinopsis AI backend API seamlessly.
- **Error Handling**: Robust error handling with retry logic for network requests.

## Installation

You can install the package using pip:

```bash
pip install sinopsis-ai
```

## Quick Start

Here’s how to get started with the Sinopsis AI SDK:

Import and Initialize the SDK

```python
from sinopsis_ai import SinopsisAI

# Initialize the SDK with your API key
api_key = "your_api_key_here"
client = SinopsisAI(api_key)
```

Start a Session

```python
# Start a session with a specific user ID
session = client.start_session(user="user_id")

# Alternatively, let the SDK generate a user ID, session ID, and conversation ID automatically
session = client.start_session()
```

Log a User Prompt

```python
# Log a user's input prompt
client.log_prompt("Hello, how are you?")
```

Log an Assistant Response

```python
# Log the assistant's response along with model details
client.log_response(
    assistant_response="I'm fine, thank you!",
    chatbot_name="ChatbotName",
    model_name="ModelName",
    model_input={"input": "Hello, how are you?"}
)
```

End the Session

```python
# End the session, ensuring all data is saved
client.end_session()
```

## Getting Help/Support
If you need help setting up or configuring the Python SDK (or anything else) please send us an email at hello@sinopsisai.com and we're ready to help you!

## Resources

## License
Licensed under the MIT license, see [LICENSE](https://github.com/Sinopsis-AI/sinopsis-ai-sdk/blob/main/LICENSE)