from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

class ChromaDB:
    def __init__(self, path: str = "chroma_db"):
        self.db = Chroma(persist_directory=path, embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"))
    
    def add_texts(self, texts: list[str], metadatas: list[dict]):
        self.db.add_texts(texts=texts, metadatas=metadatas)
        self.db.persist()

    def query(self, user_id: int, quest: str, n: int = 3) -> str:
        results = self.db.similarity_search(quest, k=n, filter={"uploader_id": str(user_id)})
        return '\n'.join([doc.page_content for doc in results])
    def get_texts_by_topic_id(self, user_id: int, topic_id: int) -> list[str]:
        results = self.db.similarity_search("", k=50, filter={"$and": [{"uploader_id": str(user_id)}, {"topic_id": topic_id}]})
        return '\n'.join([doc.page_content for doc in results])



if __name__ == "__main__":
    chroma_db = ChromaDB()
    chroma_db.add_texts(texts=["Hello world", "Hi there", "Goodbye", "Hey!"], metadatas=[{"uploader_id": "123"}, {"uploader_id": "123"}, {"uploader_id": "123"}, {"uploader_id": "123"}])
    print(chroma_db.query(user_id=123, quest="Hello"))