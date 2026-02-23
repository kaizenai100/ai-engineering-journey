from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
from commons.configs import Configs

def main():
    load_dotenv()
    prompt_template = ChatPromptTemplate.from_messages(["human","请用一句介绍{topic}"])
    model_name = os.getenv("OPENAI_MODEL", "gpt-5.2")
    base_url = os.getenv("OPENAI_BASE_URL", "")
    model = ChatOpenAI(model=model_name, base_url=base_url,temperature=1.0,default_headers=Configs.I)
    parser = StrOutputParser()
    chain = prompt_template | model | parser
    result = chain.invoke({"topic": "LangChain"})
    print(result)

if __name__ == "__main__":
    main()

