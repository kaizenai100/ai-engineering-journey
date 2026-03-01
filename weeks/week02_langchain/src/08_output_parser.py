from langchain_core.output_parsers import StrOutputParser, JsonOutputParser, PydanticOutputParser
from commons.configs import Configs
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv

def get_llm():
    load_dotenv()
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-5.2"),
        temperature=0.0,
        max_tokens=1024,
        base_url=os.environ["OPENAI_BASE_URL"],
        default_headers=Configs.IKUN_API_HEADERS
    )

def str_output_parsers(input_text):
    llm = get_llm()

    prompt = ChatPromptTemplate.from_template("简单介绍一下{topic}")

    parsers = StrOutputParser()

    chain = prompt | llm | parsers

    result = chain.invoke({"topic": input_text})
    print(result)

# 定义你期望的输出结构（Pydantic 模型）
class ScenicSpot(BaseModel):
    name: str = Field(description="景区名称")
    city: str = Field(description="所在城市")
    price: int = Field(description="门票价格（元）")
    highlights: list[str] = Field(description="核心看点，最多3个")
    

def json_output_parsers(input_text):
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个旅游信息助手。请根据用户问题返回景区信息。\n{format_instructions}"),
        ("human", "{query}")
    ])
    parsers = JsonOutputParser(pydantic_object=ScenicSpot)

    chain = prompt | llm | parsers

    result = chain.invoke({"query": input_text, "format_instructions": parsers.get_format_instructions()})

    print(result)


def pydantic_output_parsers(input_text):
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个旅游信息助手。请根据用户问题返回景区信息。\n{format_instructions}"),
        ("human", "{query}")
    ])
    parsers = PydanticOutputParser(pydantic_object=ScenicSpot)
    chain = prompt | llm | parsers
    result = chain.invoke({"query": input_text, "format_instructions": parsers.get_format_instructions()})
    print(result)

if __name__ == "__main__":
    str_output_parsers("机器学习")
    json_output_parsers("上海外滩")
    pydantic_output_parsers("上海外滩")