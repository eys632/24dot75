from langchain_community.document_loaders import TextLoader
from langchain_chroma import Chroma
from langchain_upstage import UpstageEmbeddings
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv

load_dotenv()

# def create_vector_store(collection_name, db_path, passage_embeddings=UpstageEmbeddings(model="solar-embedding-1-large-passage")):
def create_vector_store(collection_name, db_path, passage_embeddings=OpenAIEmbeddings(model="text-embedding-3-small")):
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
# 
    print("ChromaDB 내 저장된 문서 ID:", all_data.get("ids"))
    print("ChromaDB 내 저장된 메타데이터:", all_data.get("metadatas"))
# 
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
# 
    # 각 문서의 파일 이름(또는 source)을 로그에 출력
    print("[디버그] 참고 문서 목록:")
    for doc in selected_docs:
        # 만약 file_name 키가 없다면 다른 키를 확인하거나, None일 경우 '알 수 없음'을 출력함.
        file_name = doc.metadata.get("file_name") or "알 수 없음"
        print(f" - {file_name}")
# 
    return selected_docs  # 선택된 문서들의 리스트를 반환함.