# AI Companion (Replika / Paradot clone)

<img src="./readme_resources/replika.jpg" alt="replika" width="450">

### How it works

TL;DR

- We're combining a custom LangChain Chain as our AI Companion agent, and OpenAI Functions Agent as Entity Extractor for entity memory

Details

- User sends a message to the AI Companion
- Agent 1 receives the message and respond back with a LangChain `LLMChain`
- Agent 2 grabs the message and figures out whether or not it warrants a user profile update
- User receives a respond from Agent 1. Agent 2 updates the user's data at the same time.

How memory works

- Messages are kept in a `messages_history` array in `memory.py`
- Old messages are passed into the Agent's prompt but only the last K messages
- Messages older than K are summarized and stored in `summaries`, also in `memory.py` and passed into the prompt
- User's data (entities memory) is kept in entities dictionary, in `memory.py`, to provide persistent information about the user. This is what the Agent 2 will update.

### Create a new Python virtual environment

`python -m venv agent-with-memory` (Mac)

`py -m venv agent-with-memory` (Windows 11)

### Activate virtual environment

`.\agent-with-memory\Scripts\activate` (Windows)
`source agent-with-memory/bin/activate` (Mac)

### Install dependencies

`poetry install --sync` or `poetry install`

### Setup `.env` file

```text
OPENAI_API_KEY=XXXXXX

```

### Usage

`py main.py` (Windows 11)

`python main.py` (Mac)
