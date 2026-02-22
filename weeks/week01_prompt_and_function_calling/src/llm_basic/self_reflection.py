import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from commons.llm_client import OpenAIClient
client = OpenAIClient()
def main():
    # 第一步：生成
    step1 = client.chat("用Python写一个快速排序函数")
    print(f"step1:{step1}")
    print("-" * 50)

    # 第二步：自评
    step2 = client.chat(f"""请审查以下代码，指出所有问题：
    {step1}
    列出：1.bug 2.性能问题 3.可读性问题""")
    print(f"step2:{step2}")
    print("-" * 50)

    # 第三步：修正
    step3 = client.chat(f"""根据以下审查意见修正代码：
    原始代码：{step1}
    审查意见：{step2}
    输出修正后的完整代码。""")

    print(f"step3:{step3}")

if __name__ == "__main__":
    main()