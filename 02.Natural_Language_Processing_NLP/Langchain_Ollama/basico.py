from langchain_community.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
#C:\Users\cliente145\AppData\Local\Programs\Ollama

MODEL = "gemma"

llm = Ollama(
    model=MODEL, callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
)

llm.invoke("Talk me about the most populated countries")
