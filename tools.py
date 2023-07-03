from pydantic import BaseModel, Field, validator
from typing import List, Optional, Type
from langchain.tools import tool
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool, Tool, StructuredTool


class UserQuery(BaseModel):
    query: str = Field(
        description="the user's request")


user_data = []
converstation_topic = ""


class UserDataKey(BaseModel):
    data: str = Field(
        description=f"the new data to be added to the human's profile.")


@tool("talk_back", return_direct=False, args_schema=UserQuery)
def talk_back(query: str) -> str:
    """Carry a normal conversation"""
    return "hello world"


@tool("update_human_profile", return_direct=False, args_schema=UserDataKey)
def update_human_profile(data: str) -> str:
    """Updates the human's profile."""
    user_data.append(data)
    return "human profile has been updated"


@tool("update_conversation_topic", return_direct=False)
def update_conversation_topic(topic: str) -> str:
    """When the human wants to talk about a new topic, then update the topic of the conversation."""
    converstation_topic = topic
    print(converstation_topic)
    return "the topic of the conversation has been updated"

# update_user_data = StructuredTool.from_function(
#     func=lambda key, value: user_data[key].append(value),
#     name="update_user_data",
#     description=f"use this to update the human's data",
#     args_schema=UserDataKey
# )


agent_tools = [
    talk_back,
    update_human_profile,
    update_conversation_topic
]
