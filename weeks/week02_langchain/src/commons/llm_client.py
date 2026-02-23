import os
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts.base import BasePromptTemplate
from langchain_core.messages.base import BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import ToolMessage

class BaseLLMClient():
    """基类，定义统一接口"""
    
    def call(self, history:list[BaseMessage]):
        raise NotImplementedError
    def prompt_call(self, prompt:BasePromptTemplate):
        raise NotImplementedError
    def func_call(self, history:list[BaseMessage], tools):
        raise NotImplementedError


class OpenAIClient(BaseLLMClient):
    """封装LLM调用"""
    def __init__(self):
        load_dotenv()
        self.client = ChatOpenAI(
            model=os.getenv("OPENAI_MODEL", "gpt-5.2"),
            api_key=os.environ["OPENAI_API_KEY"],
            base_url=os.environ["OPENAI_BASE_URL"],
            default_headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                "X-My-App-Name": "AI-Engineering-Journey"
            }
        )

    def call(self, history:list[BaseMessage]):
        return self.client.invoke(history).content

    def prompt_call(self, prompt:BasePromptTemplate):
        return prompt | self.client | StrOutputParser()
    
    def func_call(self, history:list[BaseMessage], tools, executes):
        llm_with_tools = self.client.bind_tools(tools)
        for i in range(len(tools) + 1):
            result = llm_with_tools.invoke(history)
            history.append(result)
            if result.tool_calls:
                for tool_call in result.tool_calls:
                    tool_result = executes[tool_call["name"]].invoke(tool_call["args"]) if  executes[tool_call["name"]] else "未找到指定工具方法"
                    history.append(ToolMessage(tool_call_id=tool_call["id"], content=tool_result))
            else:
                return result.content
        return "抱歉，处理超时，请稍后重试"


class ClaudeClient(BaseLLMClient):
    """将来扩展 Claude 时在这里实现"""
    pass