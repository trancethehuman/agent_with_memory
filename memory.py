from langchain.memory import (
    ChatMessageHistory,
    ConversationSummaryMemory
)
from llm import llm_non_stream

messages_history = ChatMessageHistory()
summaries = []
entities = {
    "name": {
        "description": "This is the human's name. Human only has one name.",
        "content": [],
    },
    "likes": {
        "description": "Human's hobbies, preferences, tastes.",
        "content": [],
    },
    "dislikes": {
        "description": "Human's dislikes or hates.",
        "content": []
    },
    "traits": {
        "description": "Human's personality traits like introversion and extroversion.",
        "content": []
    },
}
summarizer = ConversationSummaryMemory(
    llm=llm_non_stream, return_messages=False)
