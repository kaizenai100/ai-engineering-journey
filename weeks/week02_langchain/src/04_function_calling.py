import os
from dotenv import load_dotenv  
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage  
import json

@tool
def get_weather(city:str) -> str:
    """
    查询天气
    """
    weathers = {
        "北京": "晴，25°C",
        "上海": "阴，35°C",
        "广州": "雨，15°C",
        "深圳": "雪，-5°C"
    }
    return weathers.get(city, "没有该城市的天气信息")


def calculator_add(num1:int, num2):
    return num1 + num2

def calculator_sub(num1, num2):
    return num1 - num2

def calculator_mul(num1, num2):
    return num1 * num2

def calculator_div(num1, num2):
    return num1 / num2

@tool
def calculator(num1:float, num2:float, operator:str) -> str:
    """
    数学计算器，支持加减乘除
    """
    operators = {
        "+": calculator_add,
        "-": calculator_sub,
        "*": calculator_mul,
        "/": calculator_div
    }
    print(f"{num1} {operator} {num2} =")
    return operators.get(operator, lambda x, y: "无效的运算符")(num1, num2)


def main(input_text) -> str:
    """
    根据用户输入，返回相应的天气信息
    """
    llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-5.2"), base_url=os.environ["OPENAI_BASE_URL"])
    llm_with_tools = llm.bind_tools([get_weather, calculator])
    messages = [
        SystemMessage(content="你是一个助手，你需要根据用户输入，调用工具，并返回结果"),
        HumanMessage(content=input_text)
    ]
    result = llm_with_tools.invoke(messages)
    messages.append(result)
    executes = {
        "get_weather": get_weather,
        "calculator":calculator,
    }
    if result.tool_calls:
        for tool_call in result.tool_calls:
            tool_result = executes[tool_call["name"]].invoke(tool_call["args"])
            messages.append(ToolMessage(tool_call_id=tool_call["id"], content=tool_result))
        
        result_msg = llm_with_tools.invoke(messages)
        return result_msg.content
    return result.content

if __name__ == "__main__":
    load_dotenv()
    print(main("北京的天气"))
    print(main("10 + 20等于几"))
