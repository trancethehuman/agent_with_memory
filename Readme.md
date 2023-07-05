# AI Companion (Replika / Paradot clone)

<img src="./readme_resources/replika.jpg" alt="replika" width="450">

### Why this is cool

- We're combining a custom LangChain Chain as our AI Companion agent, and OpenAI Functions Agent as Entity Extractor for entity memory

### Create a new Python virtual environment

`python -m venv agent-with-memory` (Mac)

`py -m venv agent-with-memory` (Windows 11)

### Activate virtual environment

`.\agent-with-memory\Scripts\activate` (Windows)

### Install dependencies

`poetry install --sync` or `poetry install`

### Setup `.env` file

```text
OPENAI_API_KEY=XXXXXX

```

### Usage

`py main.py` (Windows 11)

`python main.py` (Mac)
