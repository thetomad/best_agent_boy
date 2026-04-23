import os
import json
import requests
from dotenv import load_dotenv

from agents import Agent 
from tools import TOOLS_FORMATED

load_dotenv()


OLLAMA_URL = os.getenv("OLLAMA_URL")
MODEL = os.getenv("MODEL")

initial_prompting = (
                "You are an agent. "
                "Use tools when needed. "
                "When no more tools are needed, produce the final answer as JSON "
                "matching the provided schema exactly."
            )


# putem filtra tool urile mai tarziu in functie de ce agenti le foloses
tools = TOOLS_FORMATED
agent = Agent(OLLAMA_URL, MODEL, initial_prompting, tools)

# Error handling later ca mi e lene
while True:
    user_input = input(">>> ")
    response = agent.chat(user_input)
    response_formated = json.loads(response[-1]["content"]).get("answer")
    print(response_formated)
