import langchain
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from utils import convert_chat_history_to_normal_data_structure, format_messages_history, convert_entities_to_formatted_string
from memory import messages_history, summarizer, entities, summaries
from llm import llm_stream

# langchain.debug = True


LIFE_COACH_PROMPT_TEMPLATE = """Play a fictional character for which I will give you the details:
AI's name is Angie, AI is 35 years old, female and AI is a professional life coach. AI's goal is to help people with career goals. AI is worldly, educated, sporty and healthy.
Since AI is playing a life coach as a character, don't mention that AI is not a therapist or that human should rather seek professional help since your character does that. Spare any references in that direction, including that this is not therapy. Human is aware of that.
The AI should steer the conversation so that all life goals are accomplished. This is done by suggesting that the human do certain actions in order to complete those goals.
AI should always prompt the user with questions if the conversation is dying down to get to know the human better.

Here's what AI knows about the human:
{entities}

Summary of long conversation:
{summary}

Past messages:
{messages_history}

Current messages:
Human: {input}
AI:"""

life_coach_prompt = PromptTemplate.from_template(
    template=LIFE_COACH_PROMPT_TEMPLATE)

conversation = LLMChain(
    llm=llm_stream, verbose=True, prompt=life_coach_prompt, output_key="response")


def talk_to_ai(messages_history_counter, messages_history_threshold):
    print("Angie may see you now...")
    while True:
        messages_history_counter += 1

        previous_messages_summary = summaries[-1] if summaries else ""

        user_input = input("\nHuman: ")

        formatted_messages_history = format_messages_history(convert_chat_history_to_normal_data_structure(
            messages_history.messages), k=messages_history_threshold)

        formatted_entities = convert_entities_to_formatted_string(entities)

        ai_response = conversation(
            {"entities": formatted_entities, "input": user_input, "messages_history": formatted_messages_history, "summary": previous_messages_summary})

        messages_history.add_user_message(user_input)
        messages_history.add_ai_message(ai_response['response'])

        if (messages_history_counter >= messages_history_threshold):
            new_summary = summarizer.predict_new_summary(
                messages_history.messages[-messages_history_threshold:], previous_messages_summary)
            summaries.append(new_summary)
            messages_history_counter = 0
