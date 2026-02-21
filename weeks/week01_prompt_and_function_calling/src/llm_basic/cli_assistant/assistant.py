from commons.prompts import PromptBuilder
from commons.llm_client import OpenAIClient
from commons.tools import WeatherTool
import json

class Assistant:
    """智能助手，负责意图识别和任务分发"""

    EXTRACT_FIELDS = ["姓名", "年龄", "城市", "联系方式"]

    def __init__(self):
        self.llm = OpenAIClient()
        self.weather_tool = WeatherTool()
        self.history = [
            {
                "role": "system",
                "content": "你是一个智能助手，你的名字是ChatGPT，你需要根据用户的意图进行智能处理。"
            }
        ]

    

    def classify_intent(self, user_input):
        """意图识别"""
        prompt = PromptBuilder.intent(user_input)
        msg, _ = self.llm.call(prompt)
        return msg.content.strip()
    

    def handle_weather(self, user_input):
        """天气查询"""
        tools = [self.weather_tool.definition]
        msg, messages = self.llm.call(prompt=user_input, history=self.history, tools=tools)

        tool_call = msg.tool_calls[0]
        func_name = tool_call.function.name
        func_args = json.loads(tool_call.function.arguments)
        result = self.weather_tool.execute(func_name, func_args)

        messages.append(msg)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
        })
        msg, _ = self.llm.call(prompt='', history=messages)
        return msg.content

    def handle_extract(self, user_input):
        """信息提取"""
        fields = "、".join(self.EXTRACT_FIELDS)
        prompt = PromptBuilder.extract(user_input, fields)
        msg, _ = self.llm.call(prompt=prompt, history=self.history)
        return msg.content
    
    def handle_chat(self, user_input):
        """闲聊"""
        msg, _ = self.llm.call(prompt=user_input, history=self.history)
        return msg.content
    
    def handle(self, user_input):
        intent = self.classify_intent(user_input)
        print(f"意图：{intent}")

        handlers = {
            "查天气": self.handle_weather,
            "提取信息": self.handle_extract,
            "闲聊": self.handle_chat,
        }
        handler = handlers.get(intent)
        if handler:
            return handler(user_input)
        return "很抱歉，没能理解您的意思！"
    
    def chat(self, user_input):
        result = self.handle(user_input)
        self.history.append({"role": "user", "content": user_input})
        self.history.append({"role": "assistant", "content": result})
        return result
