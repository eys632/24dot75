import os
import glob
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.board.models import UploadedFile
from apps.board.views import vector_store
from pdf_processed.processed_documents import main
from pdf_processed.database_process import add_documents
from django.core.files import File


class Command(BaseCommand):
    help = '지정된 폴더의 모든 PDF 파일을 업로드하고 벡터 데이터베이스에 추가합니다'

    def add_arguments(self, parser):
        parser.add_argument(
            'folder_path', 
            type=str, 
            help='업로드할 파일들이 있는 폴더 경로'
        )
        parser.add_argument(
            '--user', 
            type=str, 
            default='eys632',
            help='파일을 업로드할 사용자명 (기본값: eys632)'
        )
        parser.add_argument(
            '--extensions',
            type=str,
            default='pdf,txt,doc,docx',
            help='처리할 파일 확장자 (쉼표로 구분, 기본값: pdf,txt,doc,docx)'
        )

    def handle(self, *args, **options):
        folder_path = options['folder_path']
        username = options['user']
        extensions = options['extensions'].split(',')
        
        # 폴더 존재 확인
        if not os.path.exists(folder_path):
            self.stdout.write(
                self.style.ERROR(f'폴더가 존재하지 않습니다: {folder_path}')
            )
            return
        
        # 사용자 확인
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'사용자를 찾을 수 없습니다: {username}')
            )
            return
        
        # 지원되는 파일 확장자로 파일 찾기
        files_to_process = []
        for ext in extensions:
            pattern = os.path.join(folder_path, f'*.{ext.strip()}')
            files_to_process.extend(glob.glob(pattern))
        
        if not files_to_process:
            self.stdout.write(
                self.style.WARNING(f'처리할 파일이 없습니다. 지원 확장자: {extensions}')
            )
            return
        
        self.stdout.write(f'총 {len(files_to_process)}개 파일을 처리합니다...')
        
        success_count = 0
        error_count = 0
        
        global vector_store
        
        for file_path in files_to_process:
            try:
                filename = os.path.basename(file_path)
                self.stdout.write(f'처리 중: {filename}')
                
                # 이미 업로드된 파일인지 확인
                if UploadedFile.objects.filter(file__icontains=filename).exists():
                    self.stdout.write(
                        self.style.WARNING(f'  이미 업로드된 파일: {filename} (건너뜀)')
                    )
                    continue
                
                # 파일을 Django 파일 객체로 변환
                with open(file_path, 'rb') as f:
                    django_file = File(f, name=filename)
                    
                    # UploadedFile 모델에 저장
                    uploaded_file = UploadedFile.objects.create(
                        user=user,
                        file=django_file
                    )
                
                # 텍스트 추출 및 벡터 데이터베이스에 추가
                texts = main(uploaded_file.file.path)
                if texts:
                    vector_store = add_documents(vector_store, texts)
                    uploaded_file.is_processed = True
                    uploaded_file.save()
                    success_count += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'  ✓ {filename} 처리 완료')
                    )
                else:
                    error_count += 1
                    self.stdout.write(
                        self.style.ERROR(f'  ✗ {filename} 텍스트 추출 실패')
                    )
                    
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'  ✗ {filename} 처리 중 오류: {str(e)}')
                )
        
        self.stdout.write('')
        self.stdout.write(f'처리 완료: 성공 {success_count}개, 실패 {error_count}개')
        
        if success_count > 0:
            self.stdout.write(
                self.style.SUCCESS(f'총 {success_count}개 파일이 벡터 데이터베이스에 추가되었습니다.')
            )
