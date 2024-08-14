import requests
import json
from SimplerLLM.language.llm import LLM,LLMProvider

instance = LLM.create(provider=LLMProvider.OLLAMA, model_name="Phi-3-mini-4k-instruct-Q8_0")

answer = instance.generate_response(prompt="generate a word",system_prompt="answer in arabic",)

print(answer)


