import os
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    Document,
    Settings,
)
from llama_index.core.vector_stores import (
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
)
from llama_index.core import StorageContext, load_index_from_storage
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.dashscope import DashScopeEmbedding
from llama_index.llms.dashscope import DashScope, DashScopeGenerationModels
from dotenv import load_dotenv
from llama_index.vector_stores.postgres import PGVectorStore
from sqlalchemy import make_url
import psycopg2

class LlamaIndexRAG():
    def __init__(self):
        load_dotenv()
        Settings.llm = DashScope(
            model_name="deepseek-v3.2",
            api_key=os.getenv('DASHSCOPE_API_KEY'),
        )

        # 配置 Embedding 模型（用于向量化）
        # 对比手写 RAG: client.embeddings.create(input=text, model='text-embedding-v4')
        Settings.embed_model = DashScopeEmbedding(
            model_name='text-embedding-v4',
            api_key=os.getenv('DASHSCOPE_API_KEY'),
            embed_batch_size=10  # ✅ 限制每批最多 10 条
        )

        Settings.node_parser = SentenceSplitter(chunk_size=200, chunk_overlap=30)

        self.vector_store = PGVectorStore.from_params(
                host=os.getenv('POSTGRES_HOST'),
                port=os.getenv('POSTGRES_PORT'),
                user=os.getenv('POSTGRES_USER'),
                password=os.getenv('POSTGRES_PASSWORD'),
                database='appdb',
                table_name='llama_documents',
                embed_dim=1024,
            )
        conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST'),
            port=os.getenv('POSTGRES_PORT'),
            user=os.getenv('POSTGRES_USER'),
            password=os.getenv('POSTGRES_PASSWORD'),
            database='appdb',
        )
        self.cursor = conn.cursor()

        print('✅ LLM:', Settings.llm.model_name)
        print('✅ Embedding:', Settings.embed_model.model_name)

    def get_file_docs(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, "data/scenic_data");
        documents = SimpleDirectoryReader(path, file_metadata=self.get_metadata).load_data()
        return documents

    def get_raw_documents(self):
        raw_docs = [
            {"content": "大语言模型（LLM）是基于 Transformer 架构的深度学习模型，通过海量文本数据预训练，具备理解和生成自然语言的能力。",
            "topic": "LLM", "level": "基础"},
            {"content": "RAG（检索增强生成）是一种结合检索和生成的技术，先从知识库中检索相关文档，再将其作为上下文输入给 LLM 生成回答。",
            "topic": "RAG", "level": "中级"},
            {"content": "向量数据库专门用于存储和检索高维向量，支持近似最近邻搜索（ANN），是 RAG 系统的核心组件之一。",
            "topic": "向量数据库", "level": "基础"},
            {"content": "Embedding 是将离散数据（如文本、图片）映射到连续向量空间的技术，使得语义相似的内容在向量空间中距离更近。",
            "topic": "Embedding", "level": "基础"},
            {"content": "PostgreSQL 的 pgvector 扩展支持向量数据类型和相似度搜索，可以用 SQL 直接做向量检索，无需额外部署专用向量数据库。",
            "topic": "pgvector", "level": "实战"},
            {"content": "余弦相似度衡量两个向量方向的一致性，值域为 [-1, 1]，1 表示完全相同方向，常用于文本相似度计算。",
            "topic": "数学基础", "level": "基础"},
            {"content": "Prompt Engineering 是设计和优化输入提示词的技术，通过精心构造 prompt 来引导 LLM 输出更准确、更有用的结果。",
            "topic": "Prompt", "level": "中级"},
            {"content": "Fine-tuning 是在预训练模型基础上，使用特定领域数据进行微调，使模型更好地适应特定任务或领域。",
            "topic": "Fine-tuning", "level": "高级"},
        ]
        return[
            Document(
                text=doc['content'],
                metadata={'topic': doc['topic'], 'level': doc['level']}
            )
            for doc in raw_docs
        ]
    
    def splitter(self, documents):
        # 文档切分器
        splitter = SentenceSplitter(
            chunk_size=200,      # 每块最多 200 字符（演示用，实际建议 512-1024）
            chunk_overlap=30,    # 相邻块重叠 30 字符
        )

        # 对文件加载的文档进行切分
        nodes = splitter.get_nodes_from_documents(documents)

        print(f'✅ {len(documents)} 个 Document → {len(nodes)} 个 Node')
        print(f'\n切分结果预览：')
        for i, node in enumerate(nodes):
            print(f'  Node {i}: [{len(node.text)}字符] {node.text[:60]}...')
            print(f'          metadata: {node.metadata}')
            print()

    def index(self, documents):
        index = VectorStoreIndex.from_documents(documents)
        print('✅ 向量索引构建完成')
        print(f'   索引中共 {len(documents)} 个文档')
        return index
    
    def query(self, index, query):
        query_engine = index.as_query_engine(similarity_top_k=3 )
        response = query_engine.query(query)
        print(f'❓ 问题: {query}')
        print(f'\n💡 回答:\n{response.response}')

        # 查看检索到的源文档（对比 pgvector 的 fetchall 结果）
        print(f'\n📚 引用了 {len(response.source_nodes)} 个源文档：')
        for i, node in enumerate(response.source_nodes):
            print(f'  [{i+1}] 相似度: {node.score:.4f}')
            print(f'      metadata: {node.metadata}')
            print(f'      内容: {node.text[:80]}...')
            print()

    def get_metadata(self, file_path: str) -> dict:
        file_name = os.path.basename(file_path)
        name = file_name.replace('.txt', '')
        
        return {
            "scenic_name": name,        # 景点名称，如"寒山寺"
            "file_path": file_path,
            "data_type": "scenic_info"
        }
    def semantic_search(self, index, query):
        retriever = index.as_retriever(similarity_top_k=3)
        nodes = retriever.retrieve(query)
        
        print('🔍 纯检索结果（不调 LLM，省钱省时间）：\n')
        for i, node in enumerate(nodes):
            print(f'  [{i+1}] 相似度: {node.score:.4f}')
            print(f'      topic: {node.metadata.get("topic", "N/A")}')
            print(f'      {node.text}')
            print()

    def metadata_query(self, index, query):

        # 只检索 level='基础' 的文档
        # 对比 pgvector: WHERE metadata->>'level' = '基础'
        # 对比 Milvus:   filter='level == "基础"'
        filters = MetadataFilters(
            filters=[
                MetadataFilter(
                    key='level',
                    value='基础',
                    operator=FilterOperator.EQ
                ),
            ]
        )

        filtered_retriever = index.as_retriever(
            similarity_top_k=3,
            filters=filters,
        )

        results = filtered_retriever.retrieve("文本怎么变成向量")

        print('🔍 过滤检索 [level=基础]：\n')
        for i, node in enumerate(results):
            print(f'  [{i+1}] 相似度: {node.score:.4f} | {node.metadata}')
            print(f'      {node.text}\n')


    def save_dir(self, index):
        documents = self.get_file_docs()
        index = VectorStoreIndex.from_documents(documents) 
        PERSIST_DIR = './llama_storage'

        # 保存索引到磁盘
        index.storage_context.persist(persist_dir=PERSIST_DIR)
        print(f'✅ 索引已保存到 {PERSIST_DIR}/')

        # 查看保存了什么文件
        import os
        for f in os.listdir(PERSIST_DIR):
            size = os.path.getsize(os.path.join(PERSIST_DIR, f))
            print(f'  {f}: {size:,} bytes')
        return index

    def load_dir(self):
        PERSIST_DIR = './llama_storage'

        # 加载索引
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        index = load_index_from_storage(storage_context=storage_context)
        print(f'✅ 索引已加载，共 {len(index.docstore.docs)} 个文档')
        return index
    
    def save_pgvector(self, documents):
         # 用 pgvector 作为后端构建索引
        storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        pg_index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
        )
        return pg_index

    def load_pgvector(self):
        storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        index = VectorStoreIndex.from_vector_store(
            self.vector_store,
            storage_context=storage_context
        )
        return index

    def query_pgvector(self, index, query):
        query_engine = index.as_query_engine(similarity_top_k=3)
        response = query_engine.query(query)
        print(f'❓ 问题: {query}')
        print(f'\n💡 回答:\n{response.response}')

        # 查看检索到的源文档（对比 pgvector 的 fetchall 结果）
        print(f'\n📚 引用了 {len(response.source_nodes)} 个源文档：')

    
    def select_pgvector(self):

        # 查询1：统计行数
        self.cursor.execute("SELECT COUNT(*) FROM data_llama_documents;")
        count = self.cursor.fetchone()[0]
        print(f"总行数: {count}")

        # 查询2：查看前3条记录
        self.cursor.execute("SELECT metadata_, left(text, 60) FROM data_llama_documents LIMIT 3;")
        rows = self.cursor.fetchall()
        for i, (metadata, text_preview) in enumerate(rows, 1):
            print(f"\n--- 第 {i} 条 ---")
            print(f"metadata: {metadata}")
            print(f"text前60字符: {text_preview}")

    def filtered_search(self, index, query: str, scenic_name: str = None, top_k: int = 3):
        # 只检索 level='基础' 的文档
        # 对比 pgvector: WHERE metadata->>'level' = '基础'
        # 对比 Milvus:   filter='level == "基础"'
        filters = MetadataFilters(
            filters=[
                MetadataFilter(
                    key='scenic_name',
                    value=scenic_name,
                    operator=FilterOperator.EQ
                ),
            ]
        )

        filtered_retriever = index.as_retriever(
            similarity_top_k=3,
            filters=filters,
        )

        results = filtered_retriever.retrieve(query)

        print(f'🔍 过滤检索 [scenic_name={scenic_name}]：\n')
        for i, node in enumerate(results):
            print(f'  [{i+1}] 相似度: {node.score:.4f} | {node.metadata}')
            print(f'      {node.text}\n')


