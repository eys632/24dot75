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

def load_document(file_path: str,
                  split: str = "page",
                  output_format: str = "html",
                  ocr: str = "auto",
                  coordinates: bool = True) -> List[Document]:
    """
    파일 경로에 있는 문서를 읽고, 문서 내용을 Document 자료형의 리스트로 만들어 줌
    
    매개변수:
      - file_path (str): 읽어올 문서 파일의 경로임
      - split (str): 문서를 나누는 단위임 (기본값은 한 페이지씩("page")임. 'none', 'page', 'element' 중 하나임)
      - output_format (str): 출력 형식임 (기본값은 "html"임. 'text', 'html', 'markdown' 중 하나임)
      - ocr (str): OCR(이미지에서 글자 읽기) 모드임 (기본값은 "auto"임)
      - coordinates (bool): 페이지 내 위치 정보를 포함할지 여부임 (기본값은 True임)
    
    반환값:
      - Document 객체들이 들어있는 리스트를 반환함
    """
    # 파일 경로와 옵션을 가지고 문서를 읽어오는 도구(loader)를 만듦
    loader = UpstageDocumentParseLoader(file_path,
                                          split=split,
                                          output_format=output_format,
                                          ocr=ocr,
                                          coordinates=coordinates)
    # loader.load()를 호출하여 문서를 읽어옴
    docs = loader.load()
    return docs

def filter_tegs(documents: List[Document]) -> List[Document]:
    """
    문서 리스트에서 머리글(header)이나 꼬리글(footer)이 아닌 것들만 골라서 돌려줌
    
    매개변수:
      - documents (List[Document]): 문서들이 들어있는 리스트임
    
    반환값:
      - 머리글(header)이나 꼬리글(footer)이 아닌 문서들이 들어있는 리스트임
    """
    # 각 문서의 metadata에서 'category'라는 정보를 확인함
    # 'category'가 'header'나 'footer'가 아닌 문서만 모아서 새 리스트를 만듦
    filtered_documents = [
        doc for doc in documents 
        if doc.metadata.get('category') not in ('header', 'footer')
    ]
    return filtered_documents

def main():
    """
    프로그램의 시작 부분임
    
    1. 파일 경로에 있는 문서를 읽어옴
    2. 전체 문서 개수를 출력함
    3. 머리글(header)과 꼬리글(footer)을 제외한 문서를 골라냄
    4. 필터링된 문서 개수를 출력함
    5. 예시로 첫 번째 문서의 내용을 출력함
    """
    # 읽어올 문서 파일의 경로를 설정함
    file_path = "data\Agentic Search-Enhanced.pdf"
    
    # load_document 함수를 사용하여 파일을 읽어옴
    documents = load_document(file_path=file_path, split="element")
    
    # 전체 읽어온 문서가 몇 개인지 출력함
    print(f"전체 문서 개수: {len(documents)}")
    
    # filter_non_headers 함수를 사용해서 머리글과 꼬리글이 아닌 문서를 골라냄
    filtered_documents = filter_tegs(documents)
    
    # 필터링된 문서가 몇 개인지 출력함
    print(f"헤더/푸터 제외 후 문서 개수: {len(filtered_documents)}")
    
    # 예시: 필터링된 문서가 있다면 첫 번째 문서의 내용을 출력함
    if filtered_documents:
        print("첫 번째 필터링된 문서의 내용:")
        print(filtered_documents[0].page_content)
    else:
        print("필터링된 문서가 없음")

# 이 파일이 직접 실행될 때 main() 함수를 호출함
if __name__ == "__main__":
    main()