import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from commons.configs import Configs
from pydantic import BaseModel, Field

class IntentModel(BaseModel):
    intent: str = Field(description="用户意图")
    confidence: float = Field(description="置信度 0-1")
    entities: dict = Field(description="从用户输入中提取的关键实体，如订单号、地点、数量等", default={})


def main(input_text):
    load_dotenv()
    prompt = ChatPromptTemplate.from_messages([("system", "你是意图识别器。只能返回以下意图之一：查天气、借书、退票、闲聊、投诉"),("human", "{input_text}")])

    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-5.2"),
        temperature=0.0,
        max_tokens=1024,
        base_url=os.environ["OPENAI_BASE_URL"]
    )
    structured_llm = llm.with_structured_output(IntentModel, method="function_calling")

    chian = prompt | structured_llm

    result = chian.invoke(input_text)
    print(result)
    print(result.intent)
    print(result.confidence)
    print(result.entities)

if __name__ == "__main__":
    main("我要借5本书")
