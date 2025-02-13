# 필요한 라이브러리를 가져옴
from langchain_upstage import UpstageDocumentParseLoader  # 문서를 읽어오는 도구임
from datetime import datetime  # 현재 시간을 사용하기 위해 가져옴
from dotenv import load_dotenv  # 환경 변수를 사용하기 위해 가져옴
from typing import List  # 리스트 타입을 표시할 때 사용함
from collections import namedtuple  # 이름 붙은 튜플(namedtuple)을 사용함
import os  # 환경 변수를 사용하기 위해 가져옴

load_dotenv()

# Document라는 이름의 자료형을 만듦
# 이 자료형은 문서의 정보(metadata)와 실제 내용(page_content)을 저장함
Document = namedtuple("Document", ["metadata", "page_content"])

def load_document(file_input,
                  split: str = "page",
                  output_format: str = "html",
                  ocr: str = "force",
                  coordinates: bool = False) -> List[Document]:
    """
    파일 경로에 있는 문서를 읽고, 문서 내용을 Document 자료형의 리스트로 만들어 줌
    
    매개변수:
      - file_input: 읽어올 문서 파일의 경로임
      - split (str): 문서를 나누는 단위임 (기본값은 한 페이지씩("page")임. 'none', 'page', 'element' 중 하나임)
      - output_format (str): 출력 형식임 (기본값은 "html"임. 'text', 'html', 'markdown' 중 하나임)
      - ocr (str): OCR(이미지에서 글자 읽기) 모드임 (기본값은 "auto"임)
      - coordinates (bool): 페이지 내 위치 정보를 포함할지 여부임 (기본값은 True임)
    
    반환값:
      - Document 객체들이 들어있는 리스트를 반환함
    """
    # file_input이 문자열이면 그대로 파일 경로로 사용, 그렇지 않으면 .file.path 사용
    if isinstance(file_input, str):
        actual_file_path = file_input
    else:
        actual_file_path = file_input.file.path

    loader = UpstageDocumentParseLoader(actual_file_path,
                                          split=split,
                                          output_format=output_format,
                                          ocr=ocr,
                                          coordinates=coordinates)
    docs = loader.load()
# 
    # 각 문서의 metadata에 file_name 추가 (파일명 추출)
    file_name = os.path.basename(actual_file_path)
    enhanced_docs = []
    for doc in docs:
        new_metadata = dict(doc.metadata)
        new_metadata["file_name"] = file_name
        # Document은 namedtuple("Document", ["metadata", "page_content"])
        enhanced_docs.append(Document(metadata=new_metadata, page_content=doc.page_content))
# 
    return enhanced_docs

def filter_tegs(documents: List[Document]) -> List[Document]:
    """
    문서 리스트에서 머리글(header)이나 꼬리글(footer)이 아닌 것들만 골라서 돌려줌
    
    매개변수:
      - documents (List[Document]): 문서들이 들어있는 리스트임
    
    반환값:
      - 머리글(header)이나 꼬리글(footer)이 아닌 문서들이 들어있는 리스트임
    """
    filtered_documents = [
        doc for doc in documents 
        if doc.metadata.get('category') not in ('header', 'footer')
    ]
    return filtered_documents

def main(file_path):
    """
    파일 경로에 있는 문서를 읽어와서 전처리한 후, Document 객체 리스트를 반환함.
    
    1. 파일을 읽어온 후 전체 문서 개수를 출력
    2. 머리글/푸터를 제외한 문서 개수를 출력
    3. 필터링된 문서가 있으면 이를 반환, 없으면 None을 반환
    """
    try:
        documents = load_document(file_path, split="element")
    except Exception as e:
        print(f"Error in load_document for file {file_path}: {e}")
        return []  # 예외 발생 시 빈 리스트 반환

    print(f"전체 문서 개수: {len(documents)}")
    
    filtered_documents = filter_tegs(documents)
    print(f"헤더/푸터 제외 후 문서 개수: {len(filtered_documents)}")
    
    if filtered_documents:
        return filtered_documents
    else:
        print("필터링된 문서가 없음")
        return None

# 이 파일이 직접 실행될 때 main() 함수를 호출함
# if __name__ == "__main__":
#   file_path = "data\Agentic Search-Enhanced.pdf"
#   main(file_path=file_path)