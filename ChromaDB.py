import chromadb
import fitz  # PyMuPDF
from sentence_transformers import SentenceTransformer

# ChromaDB 클라이언트 생성 (Persistent 모드)
db_path = "C:/Users/eys63/github/24dot75/chromadb"
client = chromadb.PersistentClient(path=db_path)

# 컬렉션 생성 (존재하면 가져오기)
collection_name = "school_documents"
if collection_name in [col.name for col in client.list_collections()]:
    collection = client.get_collection(collection_name)
else:
    collection = client.create_collection(collection_name)

# 임베딩 모델 로드
model = SentenceTransformer("snunlp/KR-SBERT-V40K-klueNLI-augSTS")

# PDF 파일 경로
pdf_path = "C:/Users/eys63/github/24dot75/data/SPRI_AI_Brief_2023년12월호_F.pdf"

# PDF에서 텍스트 추출
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text_list = [page.get_text("text") for page in doc]  # 각 페이지의 텍스트 추출
    return text_list

# 문서 텍스트 불러오기
texts = extract_text_from_pdf(pdf_path)

# 문서를 임베딩하고 ChromaDB에 저장
for idx, text in enumerate(texts):
    embedding = model.encode(text).tolist()
    collection.add(
        ids=[f"doc_{idx}"], 
        embeddings=[embedding], 
        metadatas=[{"page": idx, "source": pdf_path}]
    )

print(f"총 {len(texts)}개의 페이지를 ChromaDB에 저장 완료!")
