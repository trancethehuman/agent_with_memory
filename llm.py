import os
from typing import List
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

# Load .env variables
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
llm_stream = ChatOpenAI(max_retries=5, temperature=0,
                        model_name="gpt-3.5-turbo-0613", streaming=True, callbacks=[StreamingStdOutCallbackHandler()])  # type: ignore

llm_non_stream = ChatOpenAI(
    temperature=0, model_name="gpt-3.5-turbo-0613", max_retries=5,)  # type: ignore
