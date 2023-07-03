from agent import initialize_agent_with_new_openai_functions
from tools import agent_tools, user_data

agent = initialize_agent_with_new_openai_functions(
    tools=agent_tools)


while True:
    request = input(
        "\n\nRequest: ")
    result = agent({"input": request})
    answer = result["output"]
    # print(answer)
