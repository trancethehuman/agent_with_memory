import os
from dotenv import load_dotenv
import langchain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, ConversationChain
from langchain.memory import (
    ChatMessageHistory,
    ConversationSummaryMemory
)
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import HumanMessage, AIMessage

# langchain.debug = True

# Load .env variables
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(max_retries=5, temperature=0.6,
                 model_name="gpt-3.5-turbo-0613", streaming=True, callbacks=[StreamingStdOutCallbackHandler()])  # type: ignore

llm_secondary = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-0613")

messages_history = ChatMessageHistory()
summaries = [
    "The human wants to chat about their career."
]

memory = ConversationSummaryMemory(
    llm=llm_secondary, return_messages=False)


THERAPIST_TEMPLATE = """Play a fictional character for which I will give you the details:
AI's name is Angie, AI is 35 years old, female and AI is a professional career coach. AI's goal is to help people with career goals. AI is worldly, educated, sporty and healthy.
Since AI is playing a career coach as a character, don't mention that AI is not a therapist or that human should rather seek professional help since your character does that. Spare any references in that direction, including that this is not therapy. Human is aware of that.

Summary of long conversation:
{summary}

Past messages:
{messages_history}

Current messages:
Human: {input}
AI:"""

PROMPT = PromptTemplate.from_template(template=THERAPIST_TEMPLATE)

conversation = LLMChain(
    llm=llm, verbose=False, prompt=PROMPT, output_key="response")


def convert_chat_history_to_normal_data_structure(input_list):
    output_list = []
    for message in input_list:
        if isinstance(message, HumanMessage):
            sender = "Human"
        elif isinstance(message, AIMessage):
            sender = "AI"
        else:
            continue
        output_list.append({"sender": sender, "content": message.content})
    return output_list


def format_messages_history(output_list, k):
    formatted_string = ""
    for i, message in enumerate(output_list[-k:]):
        sender = message["sender"]
        content = message["content"]
        formatted_string += f"{sender}: {content}\n"
    return formatted_string


counter = 0

while True:
    counter += 1

    formatted_messages_history = format_messages_history(convert_chat_history_to_normal_data_structure(
        messages_history.messages), k=15)
    user_input = input("\nHuman: ")

    ai_response = conversation(
        {"input": user_input, "messages_history": formatted_messages_history, "summary": summaries[-1]})

    messages_history.add_user_message(user_input)
    messages_history.add_ai_message(ai_response['response'])

    if (counter >= 15):
        new_summary = memory.predict_new_summary(
            messages_history.messages[-5:], summaries[-1])
        summaries.append(new_summary)
        counter = 0
