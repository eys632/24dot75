# # 필요한 라이브러리를 가져옴
# from langchain_upstage import UpstageDocumentParseLoader  # 문서를 읽어오는 도구임
# from datetime import datetime  # 현재 시간을 사용하기 위해 가져옴
# from dotenv import load_dotenv  # 환경 변수를 사용하기 위해 가져옴
# from typing import List  # 리스트 타입을 표시할 때 사용함
# from collections import namedtuple  # 이름 붙은 튜플(namedtuple)을 사용함
# import os  # 환경 변수를 사용하기 위해 가져옴

# load_dotenv()

# # Document라는 이름의 자료형을 만듦
# # 이 자료형은 문서의 정보(metadata)와 실제 내용(page_content)을 저장함
# Document = namedtuple("Document", ["metadata", "page_content"])

# def load_document(file_input,
#                   split: str = "page",
#                   output_format: str = "html",
#                   ocr: str = "force",
#                 #   coordinates=False):
#                   coordinates: bool = False) -> List[Document]:
#     """
#     파일 경로에 있는 문서를 읽고, 문서 내용을 Document 자료형의 리스트로 만들어 줌
    
#     매개변수:
#       - file_input: 읽어올 문서 파일의 경로임
#       - split (str): 문서를 나누는 단위임 (기본값은 한 페이지씩("page")임. 'none', 'page', 'element' 중 하나임)
#       - output_format (str): 출력 형식임 (기본값은 "html"임. 'text', 'html', 'markdown' 중 하나임)
#       - ocr (str): OCR(이미지에서 글자 읽기) 모드임 (기본값은 "auto"임)
#       - coordinates (bool): 페이지 내 위치 정보를 포함할지 여부임 (기본값은 True임)
    
#     반환값:
#       - Document 객체들이 들어있는 리스트를 반환함
#     """
#     # file_input이 문자열이면 그대로 파일 경로로 사용, 그렇지 않으면 .file.path 사용
#     if isinstance(file_input, str):
#         actual_file_path = file_input
#     else:
#         actual_file_path = file_input.file.path

#     loader = UpstageDocumentParseLoader(actual_file_path,
#                                           split=split,
#                                           output_format=output_format,
#                                           ocr=ocr,
#                                           coordinates=coordinates)
#     docs = loader.load()
# # 
#     # 각 문서의 metadata에 file_name 추가 (파일명 추출)
#     file_name = os.path.basename(actual_file_path)
#     enhanced_docs = []
#     for doc in docs:
#         new_metadata = dict(doc.metadata)
#         new_metadata["file_name"] = file_name
#         # Document은 namedtuple("Document", ["metadata", "page_content"])
#         enhanced_docs.append(Document(metadata=new_metadata, page_content=doc.page_content))
# # 
#     return enhanced_docs

# 필요한 라이브러리 추가
from langchain_upstage import UpstageDocumentParseLoader
from langchain_community.document_loaders import PyPDFLoader, TextLoader  # 추가: 대체 로더
from datetime import datetime
from dotenv import load_dotenv
from typing import List
from collections import namedtuple
import os
import tempfile  # 추가: 임시 파일 처리용
import shutil    # 추가: 파일 복사용
import uuid      # 추가: 고유 파일명 생성용

load_dotenv()

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
    
    # 원본 파일명과 확장자 추출
    file_name = os.path.basename(actual_file_path)
    file_ext = os.path.splitext(file_name)[1].lower()
    
    try:
        # 방법 1: 임시 파일을 사용하여 한글 경로 문제 해결
        temp_dir = tempfile.mkdtemp()
        temp_file_name = f"temp_{uuid.uuid4().hex}{file_ext}"
        temp_file_path = os.path.join(temp_dir, temp_file_name)
        
        # 원본 파일을 임시 파일로 복사
        shutil.copy2(actual_file_path, temp_file_path)
        
        # 파일 확장자에 따라 적절한 로더 선택
        docs = []
        if file_ext.lower() in ['.pdf']:
            try:
                # 먼저 Upstage 로더 시도
                loader = UpstageDocumentParseLoader(
                    temp_file_path,
                    split=split,
                    output_format=output_format,
                    ocr=ocr,
                    coordinates=coordinates
                )
                docs = loader.load()
            except Exception as e:
                print(f"Upstage 로더 실패, PyPDFLoader로 시도: {e}")
                # 실패 시 PyPDFLoader 사용
                loader = PyPDFLoader(temp_file_path)
                docs = loader.load()
        elif file_ext.lower() in ['.txt']:
            # 텍스트 파일은 TextLoader 사용
            loader = TextLoader(temp_file_path, encoding='utf-8')
            docs = loader.load()
        else:
            # 기타 파일은 Upstage 로더 사용
            loader = UpstageDocumentParseLoader(
                temp_file_path,
                split=split,
                output_format=output_format,
                ocr=ocr,
                coordinates=coordinates
            )
            docs = loader.load()
            
        # 임시 디렉토리 제거
        shutil.rmtree(temp_dir)
        
        # 메타데이터에 원본 파일명 추가
        enhanced_docs = []
        for doc in docs:
            new_metadata = dict(doc.metadata)
            new_metadata["file_name"] = file_name
            enhanced_docs.append(Document(metadata=new_metadata, page_content=doc.page_content))
        
        return enhanced_docs
        
    except Exception as e:
        print(f"모든 로더 시도 실패: {file_name}, 오류: {e}")
        # 임시 디렉토리가 존재한다면 정리
        if 'temp_dir' in locals() and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        return []

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