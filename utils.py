from langchain.schema import HumanMessage, AIMessage


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


def convert_entities_to_formatted_string(entities):
    result = ""
    for key, value in entities.items():
        if isinstance(value['content'], list):
            if value['content']:
                result += "\n" + value['description'] + \
                    " They are " + ", ".join(value['content']) + ". "
            else:
                result += f"\nAI doesn't know the human's {key}."
        elif isinstance(value['content'], dict):
            if value['content']['is_achieved']:
                result += f"\n{value['description']} {value['content']['name']} (achieved)"
            else:
                result += f"\n{value['description']} {value['content']['name']} (not achieved)"
        else:
            result += f"\nAI doesn't know {key}."
    return result.strip()
