from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# 第一步：加载文档（指定一个目录，自动识别格式）
documents = SimpleDirectoryReader("./data/scenic_data").load_data()

# 第二步：建索引（自动切分 + embedding + 存入内存向量库）
index = VectorStoreIndex.from_documents(documents)

# 第三步：查询
query_engine = index.as_query_engine()
response = query_engine.query("寒山寺门票多少钱？")
print(response)