"""
07_agent_types.py — 三种 Agent 模式对比
同一个问题，不同配置，观察行为差异
"""
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os
from commons.configs import Configs

# ========== 工具定义（三种模式共用）==========

@tool
def get_weather(city: str) -> str:
    """查询指定城市的当前天气"""
    weathers = {"北京": "晴，25°C", "上海": "阴，35°C", "广州": "雨，15°C", "深圳": "雪，-5°C"}
    return weathers.get(city, f"{city}：暂无数据")

@tool
def calculator(num1: float, num2: float, operator: str) -> str:
    """数学计算器，支持加减乘除"""
    ops = {"+": lambda a, b: a + b, "-": lambda a, b: a - b,
           "*": lambda a, b: a * b, "/": lambda a, b: a / b}
    fn = ops.get(operator)
    return str(fn(num1, num2)) if fn else "无效运算符"


tools = [get_weather, calculator]
TEST_QUESTION = "北京和上海哪个更热？温差多少？"


def get_llm():
    load_dotenv()
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-5.2"),
        base_url=os.environ["OPENAI_BASE_URL"],
        default_headers=Configs.IKUN_API_HEADERS
    )

def print_result(name: str, result: dict):
    print(f"\n{'='*50}")
    print(f"模式: {name}")
    print(f"{'='*50}")
    for msg in result["messages"]:
        print(f"\n[{msg.type}]")
        if msg.content:
            print(f"  内容: {msg.content}")
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                print(f"  → 工具调用: {tc['name']}({tc['args']})")
    # 如果有结构化输出
    if "structured_response" in result:
        print(f"\n  📦 结构化输出: {result['structured_response']}")


# ========== 模式 1：标准 ReAct ==========
# 最自由，模型自主决策，输出格式不固定
def mode1_standard_react():
    llm = get_llm()
    agent = create_react_agent(model=llm, tools=tools)
    result = agent.invoke({"messages": [("user", TEST_QUESTION)]})
    print_result("标准 ReAct（自由输出）", result)


# ========== 模式 2：结构化输出 Agent ==========
# 推理过程和模式1一样，但最终输出必须符合指定结构
# 适合：API 接口返回、数据入库、下游系统消费
class WeatherComparison(BaseModel):
    city_a: str = Field(description="城市A名称")
    city_a_temp: float = Field(description="城市A温度(°C)")
    city_b: str = Field(description="城市B名称")
    city_b_temp: float = Field(description="城市B温度(°C)")
    hotter_city: str = Field(description="更热的城市")
    temp_diff: float = Field(description="温差(°C)")

def mode2_structured_output():
    llm = get_llm()
    agent = create_react_agent(
        model=llm,
        tools=tools,
        response_format=WeatherComparison
    )
    result = agent.invoke({"messages": [("user", TEST_QUESTION)]})
    print_result("结构化输出 Agent", result)


# ========== 模式 3：Prompt 约束 Agent ==========
# 通过 system prompt 限制 Agent 的行为模式
# 适合：企业场景中需要严格控制 Agent 行为边界
STRICT_PROMPT = """你是一个严谨的气象数据分析师。请遵守以下规则：
1. 必须先查询所有相关城市的天气数据，不能凭空编造
2. 所有数学计算必须使用 calculator 工具，不能心算
3. 回答格式必须是：
   📊 数据：[列出每个城市的天气]
   🔢 计算：[列出计算过程]
   ✅ 结论：[一句话总结]
4. 如果数据不足，明确说明而不是猜测"""

def mode3_prompt_constrained():
    llm = get_llm()
    agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=STRICT_PROMPT
    )
    result = agent.invoke({"messages": [("user", TEST_QUESTION)]})
    print_result("Prompt 约束 Agent（严格模式）", result)


# ========== 运行对比 ==========
if __name__ == "__main__":
    print("同一个问题，三种模式对比")
    print(f"问题: {TEST_QUESTION}\n")

    mode1_standard_react()
    mode2_structured_output()
    mode3_prompt_constrained()

    print(f"\n{'='*50}")
    print("对比总结：")
    print("模式1 标准ReAct：最灵活，输出格式不可控，适合探索性问答")
    print("模式2 结构化输出：推理过程一样，但最终输出是固定结构，适合API/数据管道")
    print("模式3 Prompt约束：通过指令限制行为，输出更规范，适合企业级场景")