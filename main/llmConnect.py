from supplyChainBot.main.config import llm

def llmConnectCall(message):
    response = llm.invoke(message)
    return response.content