from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from pathlib import Path
from langchain_community.document_loaders import TextLoader
import os
base_dir = os.path.dirname(os.path.abspath(__file__))

hss_docs = TextLoader(os.path.join(base_dir, "data/scenic_data/寒山寺.txt"), encoding="utf-8").load()
zzy_docs = TextLoader(os.path.join(base_dir, "data/scenic_data/拙政园.txt"), encoding="utf-8").load()
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,       # 每个 chunk 最大字符数
    chunk_overlap=50,     # 前后 chunk 重叠字符数
    separators=["\n\n", "\n", "。", "，", " ", ""]  # 切分优先级
)

chunks = splitter.split_documents(hss_docs + zzy_docs)
for i, chunk in enumerate(chunks):
    print(f"--- chunk {i} ({len(chunk.page_content)} chars) ---")
    print(chunk.page_content[:100])
    print(chunk.metadata)  