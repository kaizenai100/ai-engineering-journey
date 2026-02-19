import os
from dotenv import load_dotenv
from openai import OpenAI


def main():
    load_dotenv()
    api_key = os.environ["OPENAI_API_KEY"]
    url_ = os.environ["OPENAI_BASE_URL"]
    client = OpenAI(
        api_key=api_key,
        base_url=url_,  # 注入自定义 User-Agent
        default_headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "X-My-App-Name": "AI-Engineering-Journey"
        }
    )
    model = os.getenv("OPENAI_MODEL", "gpt-5.2")
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "reply with one short sentence: hello."}],
        # temperature=0.2,
    )
    print(resp.choices[0].message.content)


if __name__ == "__main__":
    main()
