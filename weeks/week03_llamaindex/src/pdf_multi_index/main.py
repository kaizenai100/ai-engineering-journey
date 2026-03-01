from __future__ import annotations

import os
import time
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from llama_index.core import SimpleDirectoryReader, Settings, VectorStoreIndex
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.indices.keyword_table import KeywordTableIndex
from llama_index.core.indices.tree import TreeIndex
from llama_index.llms.dashscope import DashScope
from llama_index.embeddings.dashscope import DashScopeEmbedding


PDF_PATH = Path("data/pdf/attention_is_all_you_need.pdf")
OUT_DIR = Path("outputs")
OUT_CSV = OUT_DIR / "w03d04b_evidence.csv"
OUT_MD = OUT_DIR / "w03d04b_report.md"

# QUESTIONS = [
#     "Transformer 的整体架构由哪几部分组成？",
#     "为什么要用 self-attention？相对 RNN/CNN 的主要优势是什么？",
#     "Scaled Dot-Product Attention 的公式是什么？为什么要除以 √d_k？",
#     "Multi-Head Attention 的作用是什么？多头带来什么收益？",
#     "Position Encoding 是怎么做的？（sin/cos 的形式与直觉）",
#     "论文里用了哪些正则/训练技巧？",
#     "Base vs Big 模型主要超参差异有哪些？",
#     "训练数据集是什么？用了哪些评价指标？",
#     "计算复杂度对比：self-attention vs RNN vs CNN 的对比结论是什么？",
#     "论文中的消融/对比实验有哪些关键结论？",
# ]

QUESTIONS = [
    "What are the main components of the overall Transformer architecture?",
    "Why use self-attention? What are its main advantages over RNN/CNN?",
    "What is the formula for Scaled Dot-Product Attention? Why divide by √d_k?",
    "What is the purpose of Multi-Head Attention? What benefits do multiple heads bring?",
    "How is Positional Encoding implemented? (the sin/cos form and the intuition behind it)",
    "What regularization and training techniques are used in the paper?",
    "What are the main hyperparameter differences between the Base and Big models?",
    "What training datasets were used? What evaluation metrics were applied?",
    "Computational complexity comparison: what are the conclusions for self-attention vs RNN vs CNN?",
    "What are the key conclusions from the ablation and comparison experiments in the paper?",
]



def setup_dashscope():
    load_dotenv()
    key = os.getenv("DASHSCOPE_API_KEY")
    assert key, "Missing DASHSCOPE_API_KEY in environment/.env"

    Settings.llm = DashScope(model_name="deepseek-v3.2", api_key=key)
    Settings.embed_model = DashScopeEmbedding(model_name="text-embedding-v4", api_key=key,embed_batch_size=10)

    # 先固定一个中等 chunk，保证公平对比三索引；后面再做调参实验
    Settings.node_parser = SentenceSplitter(chunk_size=200, chunk_overlap=60)

    print("LLM:", Settings.llm.model_name)
    print("EMB:", Settings.embed_model.model_name)


def load_pdf_documents(pdf_path: Path):
    assert pdf_path.exists(), f"PDF not found: {pdf_path.resolve()}"
    docs = SimpleDirectoryReader(input_files=[str(pdf_path)]).load_data()
    print("documents:", len(docs))
    preview = (docs[0].text or "")[:500]
    print("preview(500):", preview.replace("\n", " ")[:500])
    assert preview.strip(), "PDF extracted text is empty. Stop and switch loader/convert-to-txt."
    total = sum(len(d.text or "") for d in docs)
    print("total_text_len = ", total)
    nodes = Settings.node_parser.get_nodes_from_documents(docs)
    print("nodes = ", len(nodes))
    return docs


def build_indexes(documents):
    t0 = time.time()
    vector_index = VectorStoreIndex.from_documents(documents)
    print("vector_index built:", round(time.time() - t0, 2), "s")

    t0 = time.time()
    keyword_index = KeywordTableIndex.from_documents(documents)
    print("keyword_index built:", round(time.time() - t0, 2), "s")

    t0 = time.time()
    tree_index = TreeIndex.from_documents(documents)
    print("tree_index built:", round(time.time() - t0, 2), "s")

    return {
        "vector": vector_index,
        "keyword": keyword_index,
        "tree": tree_index,
    }


def retrieve_evidence(index, question: str, top_k: int = 3) -> str:
    retriever = index.as_retriever(similarity_top_k=top_k)
    nodes = retriever.retrieve(question)
    # 只取证据（省钱），不调 LLM
    lines = []
    for i, n in enumerate(nodes, 1):
        txt = (n.text or "").replace("\n", " ")
        meta = n.metadata or {}
        lines.append(f"[{i}] score={getattr(n,'score',None)} meta={meta} text={txt[:220]}")
    return "\n".join(lines)


def run_evidence(indexes: dict, questions: list[str], top_k: int = 3) -> pd.DataFrame:
    rows = []
    for idx_name, idx in indexes.items():
        for q in questions:
            evidence = retrieve_evidence(idx, q, top_k=top_k)
            rows.append(
                {
                    "index_type": idx_name,
                    "question": q,
                    "evidence_top3": evidence,
                    "score_0_1_2": "",  # 你手工填：0错/1半对/2对且完整
                    "comment": "",      # 你手工填：解析/召回/组织原因
                }
            )
    return pd.DataFrame(rows)

def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    setup_dashscope()
    documents = load_pdf_documents(PDF_PATH)
    indexes = build_indexes(documents)
    # 先跑 2 题 smoke test，确保今晚不会翻车
    df = run_evidence(indexes, QUESTIONS, top_k=8)
    df.to_csv(OUT_CSV, index=False, encoding="utf-8-sig")
    print("wrote:", OUT_CSV.resolve())


if __name__ == "__main__":
    main()  