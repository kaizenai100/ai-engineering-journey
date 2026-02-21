from commons.llm_client import OpenAIClient

# 无 CoT
prompt_direct = "一个水池有两个进水管，A管每小时注水3吨，B管每小时注水5吨。同时开两个管，多少小时能注满40吨的水池？只给答案。"

# 有 CoT
prompt_cot = "一个水池有两个进水管，A管每小时注水3吨，B管每小时注水5吨。同时开两个管，多少小时能注满40吨的水池？请一步一步思考，写出推理过程，最后给出答案。"

client = OpenAIClient()

if __name__ == "__main__":
    resp = client.call(prompt_direct)
    print(f"无 CoT:{resp.choices[0].message}")
    cot_resp = client.call(prompt_cot)
    print(f"有 CoT:{cot_resp.choices[0].message}")