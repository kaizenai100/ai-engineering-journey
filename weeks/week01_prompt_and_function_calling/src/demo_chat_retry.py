import os
import time
import uuid
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential, before_sleep_log
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("demo")

def build_client():
    return OpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.environ["OPENAI_BASE_URL"],  # 注入自定义 User-Agent
        default_headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "X-My-App-Name": "AI-Engineering-Journey"
        }
    )

@retry(
    stop=stop_after_attempt(3),                 # 总共最多 3 次（= 2 次重试）
    wait=wait_exponential(min=1, max=4),        # 指数退避：1s,2s,4s...
    before_sleep=before_sleep_log(logger, logging.INFO),
    reraise=True,
)
def call_once(client: OpenAI, model: str, trace_id: str) -> tuple[str | None, Any | None]:
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": "Reply with ONE word: hello."}],
        # temperature=0.2,
    )
    text = resp.choices[0].message.content
    usage = getattr(resp, "usage", None)
    return text, usage

def main():
    load_dotenv()
    model = os.getenv("OPENAI_MODEL", "gpt-5.2")

    trace_id = str(uuid.uuid4())
    client = build_client()

    t0 = time.time()
    out, usage = call_once(client, model, trace_id)
    elapsed_ms = int((time.time() - t0) * 1000)

    logger.info("trace_id=%s elapsed_ms=%s output=%s usage=%s", trace_id, elapsed_ms, out, usage)

if __name__ == "__main__":
    main()