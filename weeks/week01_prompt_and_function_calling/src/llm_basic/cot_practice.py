
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from commons.llm_client import OpenAIClient

# 无 CoT
prompt_direct = "一个水池有两个进水管，A管每小时注水3吨，B管每小时注水5吨。同时开两个管，多少小时能注满40吨的水池？只给答案。"

# 有 CoT
prompt_cot = "一个水池有两个进水管，A管每小时注水3吨，B管每小时注水5吨。同时开两个管，多少小时能注满40吨的水池？请一步一步思考，写出推理过程，最后给出答案。"

# 给模型一个"示范"，让它学会你想要的推理格式
prompt_fewshot_cot = """请按以下格式一步步推理：

示例：
问题：小明有5个苹果，给了小红2个，又买了3个，现在有几个？
思考：初始5个 → 给出2个剩3个 → 买入3个变6个
答案：6个

问题：一个水池有两个进水管，A管每小时注水3吨，B管每小时注水5吨。同时开两个管，多少小时能注满40吨的水池？"""

client = OpenAIClient()

if __name__ == "__main__":
    resp, _ = client.call(prompt_direct)
    print(f"无 CoT:{resp.content}")
    print("=" * 50)

    cot_resp, _ = client.call(prompt_cot)
    print(f"有 CoT:{cot_resp.content}")
    print("=" * 50)

    prompt_fewshot_cot_resp, _ = client.call(prompt_fewshot_cot)
    print(f"有 CoT:{prompt_fewshot_cot_resp.content}")