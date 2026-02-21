import os
from dotenv import load_dotenv
from openai import OpenAI
import json
def build_client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"),
                  base_url=os.getenv("OPENAI_BASE_URL"),
                  default_headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"})

def get_weather(city):
    return f"{city} 晴转多云，东风3-4级，空气质量优，18-25度，温度适宜。"

def main():
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",          # 函数名
                "description": "查询指定城市的天气",  # 告诉LLM这个函数干什么
                "parameters": {                  # 函数参数的JSON Schema
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "城市名称，如：北京、上海"
                        }
                    },
                    "required": ["city"]         # 哪些参数是必填的
                }
            }
        }
    ]
    tool_map = {
        "get_weather": get_weather
    }
    client = build_client()
    model = os.getenv("OPENAI_MODEL", "gpt-5.2")
    messages=[
            {"role": "user", "content": "苏州今天的天气怎么样？"}
        ]
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools
    )
    tool_call = resp.choices[0].message.tool_calls[0]
    func = tool_map[tool_call.function.name]
    fun_args = json.loads(tool_call.function.arguments)
    func_resp = func(**fun_args)
    messages.append(resp.choices[0].message)
    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": func_resp
        }
    )
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools
    )
    print(resp.choices[0].message.content)

if __name__ == "__main__":
    load_dotenv()
    main()