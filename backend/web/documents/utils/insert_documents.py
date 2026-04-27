import lancedb
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import LanceDB
from langchain_text_splitters import RecursiveCharacterTextSplitter
from web.documents.utils.custom_embeddings import CustomEmbeddings


def insert_documents():
    loader = TextLoader('./web/documents/data.txt', encoding='utf-8')
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    print("文本切分完成，切分后的文本块数量：", len(texts))

    embeddings = CustomEmbeddings()
    db = lancedb.connect('./web/documents/lancedb_storage')
    vector_db = LanceDB.from_documents(
        documents=texts,
        embedding=embeddings,
        connection=db,
        table_name='my_knowledge_base',
        mode='overwrite'
    )
    print(f"已插入 {vector_db._table.count_rows()} 条文本块到 LanceDB 中。")


