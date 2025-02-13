import os
import logging
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from apps.board.models import UploadedFile

# ChromaDB의 전역 vector_store를 가져옵니다.
# (vector_store가 apps/board/views.py 등에서 정의되어 있다면 해당 경로로 import 하세요)
from apps.board.views import vector_store, add_documents
from pdf_processed.processed_documents import main

logger = logging.getLogger(__name__)

def remove_documents_by_file_name(vector_store, file_name):
    """
    ChromaDB에 저장된 모든 문서 중, 메타데이터에 file_name이 일치하는 문서들을 삭제합니다.
    """
    all_data = vector_store.get()
    ids_to_remove = [
        doc_id for doc_id, meta in zip(
            all_data.get("ids", []), 
            all_data.get("metadatas", [])
        )
        if meta.get("file_name") == file_name
    ]
    if ids_to_remove:
        vector_store.delete(ids=ids_to_remove)
        logger.info(f"{file_name} 관련 문서 {len(ids_to_remove)}개 삭제됨.")

@receiver(post_delete, sender=UploadedFile)
def on_uploaded_file_delete(sender, instance, **kwargs):
    """
    UploadedFile 모델 인스턴스가 삭제될 때, 해당 파일과 관련된 ChromaDB 문서들을 삭제합니다.
    """
    file_name = os.path.basename(instance.file.name)
    remove_documents_by_file_name(vector_store, file_name)

@receiver(post_save, sender=UploadedFile)
def on_uploaded_file_save(sender, instance, created, **kwargs):
    """
    새 UploadedFile 모델 인스턴스가 생성되면, 해당 파일을 즉시 임베딩하여 ChromaDB에 추가합니다.
    """
    if created:
        file_path = instance.file.path
        texts = main(file_path)
        if texts:
            global vector_store
            vector_store = add_documents(vector_store, texts)
            logger.info(f"{os.path.basename(file_path)} 새 문서 임베딩 완료.")
