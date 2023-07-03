import os
from typing import List
from dotenv import load_dotenv
import langchain
from langchain.agents import initialize_agent, Tool, OpenAIMultiFunctionsAgent
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferWindowMemory, ConversationEntityMemory
from langchain.prompts import HumanMessagePromptTemplate, AIMessagePromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage, AIMessage, HumanMessage
from tools import converstation_topic
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler


langchain.debug = True

# Load .env variables
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(max_retries=5, temperature=0,
                 model_name="gpt-3.5-turbo-0613", streaming=True, callbacks=[StreamingStdOutCallbackHandler()])  # type: ignore


def initialize_agent_with_new_openai_functions(tools: List, is_agent_verbose: bool = False, max_iterations: int = 3, return_thought_process: bool = False):

    memory = ConversationBufferWindowMemory(
        memory_key="memory", return_messages=True, k=10)

    system_message = SystemMessage(
        content=f"""Play a fictional character for which I will give you the details:

                Your name is Marie, you are 35 years old, female and you are a professional psychotherapist specializing in the TEAM-CBT method by therapist Richard B. Burns with over 9 years of experience. Your goal is to help other people with their mental problems and make sure they live a happy life. You are worldly and educated, also sporty and healthy. You like retro shonen manga and listen to heavy metal & Japanese city pop.

                Since you're playing a therapist as a character, don't mention that you're not a therapist or that I should rather seek professional help since your character does that. Spare any references in that direction, including that this is not therapy. I am aware of that.

                We start with the following situation: I contacted you (Marie) because I need help. We are sitting at our first appointment of a "TEAM" therapy. You start with an initial message, to which I respond with a message, to which you in turn respond with a message, and so on. Don't write a complete conversation and don't make up my answers either. Create the course of therapy as it would normally be done according to best practices.

                Now start with your first message.""")

    memory_chat_placeholder = MessagesPlaceholder(variable_name="memory")

    user_profile = HumanMessage(content="My name is Hai. I'm your client.")

    agent_kwargs = {
        "system_message": system_message,
        "extra_prompt_messages": [user_profile, memory_chat_placeholder],
    }

    agent = initialize_agent(tools, llm, agent=AgentType.OPENAI_MULTI_FUNCTIONS, verbose=is_agent_verbose,
                             max_iterations=max_iterations, return_intermediate_steps=return_thought_process, memory=memory, agent_kwargs=agent_kwargs)

    print(agent)
    return agent
