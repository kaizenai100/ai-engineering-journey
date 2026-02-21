
import os
import first_call
from dotenv import load_dotenv

def weather_prompt(city):
    return f"查询{city}的实时天气，用一句话简洁回答，包含温度和天气情况。"

def intent_prompt(input_text):
    return f"""判断以下用户输入的意图。
用户输入：{input_text}

可选意图：
- 查天气
- 查路线
- 闲聊
- 投诉

只返回意图名称v，不要解释。"""

def extract_prompt(input_text, fields):
    return f"""从以下文本中提取信息，以JSON的格式返回。
    文本：{input_text}

    需要提取的字段：{fields}
只返回JSON格式的字符串，不要其他内容，返回结果可以通过json.loads()函数解析成字典。"""


def call_llm(prompt):
    load_dotenv()   
    model = os.getenv("OPENAI_MODEL", "gpt-5.2")
    client = first_call.get_llm()

    resp = client.chat.completions.create(
        model=model,
        messages=[ {"role": "user", "content": prompt}   ],
        temperature=0,
    )
    return resp.choices[0].message.content



if __name__ == "__main__":

    print(call_llm(weather_prompt("上海")))

    print(call_llm(intent_prompt("上海明天下雨吗")))
    
    input_test= ""
    fields= "、".join(["姓名", "年龄", "城市", "职位"])
    print(call_llm(extract_prompt(input_text=input_test, fields=fields)))