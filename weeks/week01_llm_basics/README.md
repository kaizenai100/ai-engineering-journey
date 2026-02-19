# Week 01 - LLM Basics

## Goal
Build a minimal `llm_client` with retry/logging and a small prompt library.

## Today (D1)
- B1: repo skeleton + docs
- B2: minimal chat completion call
- B3: retry + timeout (at least retry)
- B4: trace_id + elapsed_ms + usage placeholder

## Deliverables
- runnable demo script
- basic logs

## Environment

### Option A: Conda (recommended)
```bash
conda create -n ai-engineering-journey python=3.12.11 -y
conda activate ai-engineering-journey

pip install openai python-dotenv
pip install tenacity
```

### 完成一次 LLM 调用
```bash
python weeks/week01_llm_basics/src/demo_chat.py 
```

### 加超时/重试/记录日志
```bash
python weeks/week01_llm_basics/src/demo_chat_retry.py 
```