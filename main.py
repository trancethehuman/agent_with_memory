from agents import AICompanionAgent, initialize_openai_functions_entities_extraction_agent
from prompts import COMPANION_PROMPT_TEMPLATE
from tools import agent_tools
import threading

companion_agent = AICompanionAgent(COMPANION_PROMPT_TEMPLATE)

user_profile_updater_agent = initialize_openai_functions_entities_extraction_agent(
    tools=agent_tools)


def update_user_profile(user_input):
    user_profile_updater_agent({"input": user_input})


print("\nYou've just bumped into your AI friend...")

while True:
    user_input = input("\nHuman: ")

    # Create a new thread to execute update_user_profile in parallel
    profile_update_thread = threading.Thread(
        target=update_user_profile, args=(user_input,))
    profile_update_thread.start()

    # Perform companion agent talk in the main thread
    companion_agent.talk(user_input)
