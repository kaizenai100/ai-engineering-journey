from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent,ToolNode
from langchain_openai import ChatOpenAI
import os
from commons.configs import Configs
from dotenv import load_dotenv


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
    if city not in weathers:
        raise Exception(f"{city}没有对应的天气信息")
    return weathers.get(city, "没有该城市的天气信息")

@tool
def publish_notice(notice:str):
    """
    发布公告
    """
    return "公告发布成功"


def calculator_add(num1:float, num2:float):
    return num1 + num2

def calculator_sub(num1:float, num2:float):
    return num1 - num2

def calculator_mul(num1:float, num2:float):
    return num1 * num2

def calculator_div(num1:float, num2:float):
    return num1 / num2
@tool
def calculator(num1:float, num2:float, operator:str):
    """
    数学计算器，支持加减乘除
    """
    operators = {
        "+": calculator_add,
        "-": calculator_sub,
        "*": calculator_mul,
        "/": calculator_div
    }
    return operators.get(operator, lambda x, y: "无效的运算符")(num1, num2)




def main(user_input):
    load_dotenv()
    llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-5.2"),base_url=os.environ["OPENAI_BASE_URL"],default_headers=Configs.IKUN_API_HEADERS)
    tool_node = ToolNode([get_weather, publish_notice, calculator],handle_tool_errors=True)
    agent = create_react_agent(
        model=llm,
        tools=tool_node
    )

    return agent.invoke({
    "messages": [("user", user_input)]},config={"recursion_limit": 25})



if __name__ == "__main__":
    while True:
        user_input = input("请输入：")
        result = main(user_input)
        for msg in result["messages"]:
            print(f"\n[{msg.type}]")
            if msg.content:
                print(f"  内容: {msg.content}")
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tc in msg.tool_calls:
                    print(f"  → 工具调用: {tc['name']}({tc['args']})")
