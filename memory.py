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
        "description": "These are hobbies, preferences, tastes.",
        "content": [],
    },
    "dislikes": {
        "description": "These are things the human dislikes or hates.",
        "content": []
    },
    "traits": {
        "description": "These are personality traits like introversion and extroversion.",
        "content": []
    },
}
summarizer = ConversationSummaryMemory(
    llm=llm_non_stream, return_messages=False)
