from llamaIndex_rag import LlamaIndexRAG

def run_file_docs(rag:LlamaIndexRAG, query:str, ):
    print("=" * 50 + "get_file_docs" + "=" * 50)
    file_docs = rag.get_file_docs()
    print("=" * 50 + "splitter_file_documents" + "=" * 50)
    rag.splitter(file_docs)
    print("=" * 50 + "index" + "=" * 50)
    index = rag.index(file_docs)
    rag.query(index, query)
    rag.semantic_search(index, query)
    rag.metadata_query(index, query)


def run_row_docs(rag:LlamaIndexRAG, query:str):
    print("=" * 50 + "get_raw_documents" + "=" * 50)
    raw_docs= rag.get_raw_documents()
    print("=" * 50 + "splitter_raw_documents" + "=" * 50)
    rag.splitter(raw_docs)
    print("=" * 50 + "splitter_raw_documents" + "=" * 50)
    index = rag.index(raw_docs)
    rag.query(index, query)
    rag.semantic_search(index, query)
    rag.metadata_query(index, query)



def save_pg(rag:LlamaIndexRAG, query:str):
    file_docs = rag.get_file_docs()
    indix = rag.save_pgvector(file_docs)
    rag.query_pgvector(indix, query)


def filtered_pg(rag:LlamaIndexRAG, query:str, scenic_name:str = None):
    file_docs = rag.get_file_docs()
    indix = rag.load_pgvector()
    rag.filtered_search(indix, query, scenic_name) if scenic_name else rag.query_pgvector(indix, query)

def save_dir(rag:LlamaIndexRAG, query:str):
    file_docs = rag.get_file_docs()
    index = rag.save_dir(file_docs)
    rag.query(index, query)

def query_dir(rag:LlamaIndexRAG, query:str):
    index = rag.load_dir()
    rag.query(index, query)



if __name__ == '__main__':
    rag = LlamaIndexRAG()
    # save_pg(rag=rag, query="寒山寺的票价是多少？")
    # run_file_docs(rag, "寒山寺的票价是多少？")
    # run_row_docs(rag, "什么是大语言模型")
    filtered_pg(rag, "寒山寺的票价是多少？")
    print("-" * 50) 
    filtered_pg(rag, "寒山寺的票价是多少？",scenic_name="寒山寺")