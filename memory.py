from langchain.memory import (
    ChatMessageHistory,
    ConversationSummaryMemory
)
from llm import llm_non_stream

messages_history = ChatMessageHistory()
summaries = []
entities = {
    "name": {
        "description": "The human's name is",
        "content": ["James"],
    },
    "likes": {
        "description": "The human likes",
        "content": ["singing", "dancing", "play pretend"],
    },
    "dislikes": {
        "description": "The human doesn't like or hate",
        "content": []
    },
    "traits": {
        "description": "The human's personality traits are",
        "content": ["extroverted"]
    },
    "goals": {
        "description": "The human's life goals are",
        "content": []
    }
}

summarizer = ConversationSummaryMemory(
    llm=llm_non_stream, return_messages=False)

messages_history_counter = 0
messages_history_threshold = 10
