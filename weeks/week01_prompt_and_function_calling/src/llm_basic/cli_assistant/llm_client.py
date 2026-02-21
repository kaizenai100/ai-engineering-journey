import os
import json
from dotenv import load_dotenv
from openai import OpenAI

class BaseLLMClient:
    """基类，定义统一接口"""
    
    def call(self, prompt, history=None, tools=None):
        raise NotImplementedError


class OpenAIClient(BaseLLMClient):
    """封装LLM调用"""
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
            base_url=os.environ["OPENAI_BASE_URL"],
            default_headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                "X-My-App-Name": "AI-Engineering-Journey"
            }
        )
        self.model = os.getenv("OPENAI_MODEL", "gpt-5.2")

    def call(self, prompt, history=None, tools=None):
        messages = []
        if history:
            messages.extend(history)
        if prompt:
            messages.append({"role": "user", "content": prompt})

        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0,
            tools=tools
        )
        return resp.choices[0].message, messages

class ClaudeClient(BaseLLMClient):
    """将来扩展 Claude 时在这里实现"""
    pass