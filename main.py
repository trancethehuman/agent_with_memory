from agents import AICompanionAgent, EntitiesExtractionAgent
from memory import messages_history
from prompts import COMPANION_PROMPT_TEMPLATE
from tools import entities_extraction_tools
import threading

companion_agent = AICompanionAgent(COMPANION_PROMPT_TEMPLATE, verbose=False)

user_profile_updater = EntitiesExtractionAgent(
    tools=entities_extraction_tools)

print("\nYou've just bumped into your AI friend...")

while True:
    user_input = input("\nHuman: ")

    # Create a new thread to execute update_user_profile in parallel
    profile_update_thread = threading.Thread(
        target=user_profile_updater.update_user_profile, args=(user_input,))
    profile_update_thread.start()

    # Perform companion agent talk in the main thread
    print(companion_agent.talk(user_input))
