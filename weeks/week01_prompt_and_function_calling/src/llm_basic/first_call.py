from openai import OpenAI
from dotenv import load_dotenv
import os
def get_llm():
    return OpenAI(
        api_key=os.environ["OPENAI_API_KEY"], 
        base_url=os.environ["OPENAI_BASE_URL"],
        default_headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "X-My-App-Name": "AI-Engineering-Journey"
        })
    
def main(temperature):
    load_dotenv()
    client = get_llm()
    model = os.getenv("OPENAI_MODEL", "gpt-5.2")
    result = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "你是一个毒舌美食评论家，说话刻薄但有道理"},
            {"role": "user", "content": "我做了一碗番茄炒蛋"},
            {"role": "assistant", "content": "番茄炒蛋都能拿出来说，你是不是对烹饪有什么误解？"},
            {"role": "user", "content": "那你觉得怎么改进？"},
        ],
        temperature=temperature,
    )
    print(f"\n--- temperature={temperature} ---")
    print(result.choices[0].message.content)

if __name__ == "__main__":
    main(0)
    main(0.7)
    main(1.5)
