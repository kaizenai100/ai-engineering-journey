import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from commons.configs import Configs
from langchain_core.output_parsers import StrOutputParser

def main(input_text):
    load_dotenv()
    prompt_template = ChatPromptTemplate.from_messages([("human", """判断以下用户输入的意图。
    用户输入：{input_text}

    可选意图：
    - 查天气
    - 提取信息
    - 闲聊
    - 投诉

    只返回意图名称，不要解释。""")])
    model = os.getenv("OPENAI_MODEL", "gpt-5.2")
    base_url = os.getenv("OPENAI_BASE_URL", "")
    llm = ChatOpenAI(model=model, base_url=base_url,default_headers=Configs.IKUN_API_HEADERS)
    parser = StrOutputParser()
    chain = prompt_template | llm | parser
    result = chain.invoke({"input_text": input_text})
    print(result)

if __name__ == "__main__":
    tests = [
    "北京今天天气怎么样",
    "我叫张三，手机号13800138000",
    "你好呀",
    "你们服务太差了"
]
for t in tests:
     main(t)