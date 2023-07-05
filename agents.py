import langchain
from typing import Dict, List
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.agents import initialize_agent, AgentType
from langchain.schema import SystemMessage
from utils import convert_chat_history_to_normal_data_structure, format_messages_history, convert_entities_to_formatted_string
from memory import messages_history, summarizer, entities, summaries
from llm import llm_stream, llm_non_stream

# langchain.debug = True


class AICompanionAgent:
    def __init__(self, prompt_template, messages_history_threshold: int = 15, verbose: bool = False):
        self.prompt = PromptTemplate.from_template(template=prompt_template)
        self.conversation_chain = LLMChain(
            llm=llm_non_stream, verbose=True, prompt=self.prompt, output_key="response")
        self.messages_history_threshold = messages_history_threshold
        self.messages_history_counter = 0
        self.verbose = verbose

    def talk(self, user_input: str):
        self.messages_history_counter += 1

        previous_messages_summary = summaries[-1] if summaries else ""

        formatted_messages_history = format_messages_history(convert_chat_history_to_normal_data_structure(
            messages_history.messages), k=self.messages_history_threshold)

        formatted_entities = convert_entities_to_formatted_string(entities)

        self.conversation_chain.verbose = self.verbose

        ai_response = self.conversation_chain(
            {"entities": formatted_entities, "input": user_input, "messages_history": formatted_messages_history, "summary": previous_messages_summary})

        messages_history.add_user_message(user_input)
        messages_history.add_ai_message(ai_response['response'])

        if (self.messages_history_counter >= self.messages_history_threshold):
            new_summary = summarizer.predict_new_summary(
                messages_history.messages[-self.messages_history_threshold:], previous_messages_summary)
            summaries.append(new_summary)
            self.messages_history_counter = 0

        return ai_response['response']


class EntitiesExtractionAgent:
    def __init__(self, tools: List, is_agent_verbose: bool = False, max_iterations: int = 3, return_thought_process: bool = False):
        entities_extraction_message = SystemMessage(
            content=f"""Use your judgement and pick out the information you need from the human's new message, based on the following list of human's data:
            {entities}
            Use a tool to update the human's profile if new information is presented. Don't update if there isn't new information from the human's message.
            .""")

        agent_kwargs = {
            "system_message": entities_extraction_message,
        }

        self.agent = initialize_agent(tools, llm_non_stream, agent=AgentType.OPENAI_FUNCTIONS, verbose=is_agent_verbose,
                                      max_iterations=max_iterations, return_intermediate_steps=return_thought_process, agent_kwargs=agent_kwargs)

    def update_user_profile(self, user_input):
        return self.agent({"input": user_input})
