'''
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_upstage import UpstageEmbeddings
from dotenv import load_dotenv

load_dotenv()

def create_vector_store(collection_name, db_path, passage_embeddings=UpstageEmbeddings(model="solar-embedding-1-large-passage")):
    """
    백터 스토어를 생성함.
    매개변수:
      - collection_name (str): 컬렉션 이름임.
      - db_path (str): 로컬 데이터 저장 경로임.
      - passage_embeddings (Callable): 텍스트를 임베딩하는 함수임.
    반환값:
      - 생성된 백터 스토어 객체.
    """
    # Chroma 객체를 생성함.
    vector_store = Chroma(
        collection_name=collection_name,  # 컬렉션 이름을 지정함.
        embedding_function=passage_embeddings,  # 임베딩 함수를 지정함.
        persist_directory=db_path,  # 데이터 저장 경로를 지정함.
    )
    # 생성된 백터 스토어 객체를 반환함.
    return vector_store

def add_documents(vector_store, documents):
    """
    문서 DB에 새로운 문서를 추가함.
    매개변수:
      - vector_store (Chroma): 문서 저장소 객체임.
      - documents (List[Document]): 추가할 문서들의 리스트임.
    반환값:
      - 문서가 추가된 vector_store 객체.
    """
    all_data = vector_store.get()  # vector_store에서 기존 문서 데이터를 가져옴.
    # print(f"[디버그] 현재 저장된 문서 개수 : {len(all_data['ids'])}, 저장 할 문서 개수 : {len(documents)}")  # 현재 문서 개수와 추가할 문서 개수를 디버그로 출력함.
    
    strat = len(all_data['ids']) + 1  # 시작 인덱스를 기존 문서 개수 + 1로 설정함.
    end = len(documents) + len(all_data['ids']) + 1  # 끝 인덱스를 기존 문서 개수와 추가할 문서 개수를 합산 후 1 더하여 설정함.
    uuids = [str(i) for i in range(strat, end)]  # 새 문서의 id 리스트를 숫자 문자열로 생성함.
    # print(f"[디버그] uuids : {uuids}")  # 생성된 uuids를 디버그로 출력함.
    
    vector_store.add_documents(documents=documents, ids=uuids)  # vector_store에 새 문서와 id 리스트를 추가함.

    return vector_store  # 변경된 vector_store 객체를 반환함.

def select_docs(db, query):
    """
    데이터베이스에서 쿼리에 대한 문서를 선택함.
    매개변수:
      - db (Chroma): 문서 저장소 객체임.
      - query (str): 쿼리 문장임.
    반환값:
      - 선택된 문서들의 리스트.
    """
    # 쿼리를 사용하여 문서를 선택함.
    print(f"[디버그] db : {db}")
    retriever = db.as_retriever()
    selected_docs = retriever.invoke(query)
    return selected_docs  # 선택된 문서들의 리스트를 반환함.

def check_stored_documents(vector_store):
    """ChromaDB에 저장된 문서 개수를 확인하는 함수"""
    all_data = vector_store.get()
    print(f"[디버그] 저장된 문서 개수: {len(all_data['ids'])}")
    print(f"[디버그] 저장된 문서 내용 예시: {all_data['documents'][:3]}")  # 첫 3개만 출력

if __name__ == "__main__":
    db = create_vector_store(collection_name="document_embeddings", db_path="pdf_processed/chroma_langchain_db")
    
    check_stored_documents(db)
'''
from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_upstage import UpstageEmbeddings
from dotenv import load_dotenv
#from processed_documents import load_document
from pdf_processed.processed_documents import load_document


load_dotenv()

def create_vector_store(collection_name, db_path, passage_embeddings=UpstageEmbeddings(model="solar-embedding-1-large-passage")):
    """
    백터 스토어를 생성함.
    """
    vector_store = Chroma(
        collection_name=collection_name,
        embedding_function=passage_embeddings,
        persist_directory=db_path,
    )
    return vector_store

def add_documents(vector_store, documents):
    """
    문서 DB에 새로운 문서를 추가함.
    """
    all_data = vector_store.get()
    strat = len(all_data['ids']) + 1
    end = len(documents) + len(all_data['ids']) + 1
    uuids = [str(i) for i in range(strat, end)]
    vector_store.add_documents(documents=documents, ids=uuids)
    return vector_store

def select_docs(db, query):
    """
    데이터베이스에서 쿼리에 대한 문서를 선택함.
    """
    retriever = db.as_retriever()
    selected_docs = retriever.invoke(query)
    return selected_docs

def check_stored_documents(vector_store):
    """ChromaDB에 저장된 문서 개수를 확인하는 함수"""
    all_data = vector_store.get()
    print(f"[디버그] 저장된 문서 개수: {len(all_data['ids'])}")
    print(f"[디버그] 저장된 문서 내용 예시: {all_data['documents'][:3]}")

if __name__ == "__main__":
    db = create_vector_store(collection_name="document_embeddings", db_path="pdf_processed/chroma_langchain_db")
    
    # 문서 불러오기
    file_path = "pdf_processed/data/SPRI_AI_Brief_2023년12월호_F.pdf"
    docs = load_document(file_path=file_path, split="element")
    print(f"[디버그] 불러온 문서 개수: {len(docs)}")
    
    # 문서 추가
    db = add_documents(db, docs)
    
    # 저장된 문서 확인
    check_stored_documents(db)

"""    
    # 테스트할 질문
    query = "미국의 AI 관련 정책과 법제 변화"

    # 문서 검색
    retrieved_docs = select_docs(db, query)
    print(f"[디버그] 검색된 문서 개수: {len(retrieved_docs)}")
    print(f"[디버그] 검색된 문서 예시: {retrieved_docs[:3]}")  # 상위 3개만 출력
"""