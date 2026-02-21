import os
import json
from dotenv import load_dotenv
from openai import OpenAI

def get_llm():
    return OpenAI(
        api_key=os.environ["OPENAI_API_KEY"], 
        base_url=os.environ["OPENAI_BASE_URL"],
        default_headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "X-My-App-Name": "AI-Engineering-Journey"
        })

load_dotenv()
client = get_llm()
model = os.getenv("OPENAI_MODEL", "gpt-5.2")
def weather_prompt(city):
    return f"查询{city}的实时天气，用一句话简洁回答，包含温度和天气情况。"

def intent_prompt(input_text):
    return f"""判断以下用户输入的意图。
用户输入：{input_text}

可选意图：
- 查天气
- 提取信息
- 闲聊
- 投诉

只返回意图名称，不要解释。"""

def extract_prompt(input_text, fields):
    return f"""从以下文本中提取信息，以JSON的格式返回。
    
    文本：{input_text}
    
    提取的字段全部选项：{fields}
    
    注意：文本中可能包含用户的问题，请根据问题意图只提取相关字段，而不是提取全部字段。
    只返回JSON格式的字符串，不要其他内容，返回结果可以通过json.loads()函数解析成字典。"""

def get_weather(city):
    return f"{city} 晴转多云，东风3-4级，空气质量优，18-25度，温度适宜。"


def get_tools() -> tuple[list, dict]:
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "查询天气",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "city": {
                            "type": "string",
                            "description": "城市名称"
                        }
                    },
                    "required": ["city"]
                }
            }
        }
    ]
    return tools, {
        "get_weather": get_weather
    }


def call_llm(prompt, history=None, tools = None) -> tuple[str | None, list | None]: 
    model = os.getenv("OPENAI_MODEL", "gpt-5.2")
    messages = []
    if history:
        messages.extend(history)
    if prompt:
        messages.append({"role": "user", "content": prompt})
    resp = client.chat.completions.create(
        model=model,
        messages= messages,
        temperature=0,
        tools=tools
    )
    return resp.choices[0].message, messages

def classify_intent(user_input):
    prompt = intent_prompt(user_input)
    msg, messages = call_llm(prompt)
    return msg.content

def handle(user_input, history):
    intent = classify_intent(user_input)
    print(f"意图：{intent}")
    if intent == "查天气":
        tools, toolsMapping = get_tools()
        msg, messages = call_llm(prompt = user_input, history=history, tools=tools)
        tool_call = msg.tool_calls[0]
        func_name = tool_call.function.name
        func_args = json.loads(tool_call.function.arguments)
        func = toolsMapping[func_name]
        weather = func(**func_args)
        messages.append(msg)
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": weather
            }
        )
        msg, messages = call_llm(prompt='',history=messages)
        return msg.content
    elif intent == "提取信息":
        fields= "、".join(["姓名", "年龄", "城市","联系方式"])
        prompt = extract_prompt(user_input, fields)
        msg, messages = call_llm(prompt = prompt, history = history)
        return msg.content
    elif intent == "闲聊":
        msg, messages = call_llm(prompt = user_input, history = history)
        return msg.content
    else:
        return "很抱歉，没能理解您的意思！"
    

if __name__ == "__main__":
    load_dotenv() 
    history = [
        {
            "role": "system",
            "content": "你是一个智能助手，你的名字是ChatGPT，你需要根据用户的意图进行智能处理。"
        }
    ]
    while True:
        user_input = input("请输入：")
        result = handle(user_input, history)
        history.append({"role": "user", "content": user_input})
        history.append({"role": "assistant", "content": result})
        print(result)