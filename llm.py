from langchain.chat_models import ChatOpenAI

llm_non_stream = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-0613")
