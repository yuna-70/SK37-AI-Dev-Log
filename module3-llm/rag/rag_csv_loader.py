"""TIL: CSVLoader로 표 형식 데이터 불러오기 (2026-11-18) — 개념 설명은 README.md 참고"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import CSVLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma


# 1. 환경 설정
env_file_path = ".env"
output = load_dotenv(env_file_path)

print(output)


# 2. CSV 로드 및 Document 자료형으로 변환
## CSVLoader는 "행" 단위로 Document를 만듦 -> 30행이면 Document 30개
## 매개 변수
##   content_columns: 본문(page_content)에 포함할 컬럼 지정
##   metadata_columns: 메타데이터로 뺄 컬럼 지정
## 표는 이미 한 행이 하나의 의미 단위라서 별도의 분할 과정이 필요 없음
csv_path = "ChatBotData_sample.csv"

loader = CSVLoader(
    file_path=csv_path,
    encoding="utf-8",
    content_columns=["Q", "A"],
    ## label 컬럼은 검색 대상이 아니라 분류 정보이므로 메타데이터로 분리
    metadata_columns=["label"],
)

docs = loader.load()

print(f"로드된 총 문서 수: {len(docs)}개")
print("-" * 80)
print(f"[첫 번째 Document 본문(page_content)]\n{docs[0].page_content}")
print("-" * 80)
## metadata에 source(파일명), row(행 번호), label이 함께 들어감
print(f"[첫 번째 Document 메타데이터(metadata)]\n{docs[0].metadata}")


# 3. 임베딩 모델 생성
model_name = "text-embedding-3-small"
model = OpenAIEmbeddings(model=model_name)


# 4. 벡터 저장소 생성 또는 불러오기
chroma_path = "chroma_db_csv"

if os.path.exists(chroma_path) and os.listdir(chroma_path):
    vectorstore = Chroma(
        persist_directory=chroma_path,
        embedding_function=model,
    )
    print("기존 벡터 저장소를 성공적으로 불러왔습니다.")

else:
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=model,
        persist_directory=chroma_path,
    )
    print("신규 벡터 저장소를 생성하고 저장했습니다.")


# 5. 검색 도구 생성
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})


# 6. 검색 도구 성능 테스트
user_query = "가족 여행 갈거야. 기대가 많이 돼"
output = retriever.invoke(user_query)

print(f"검색 결과: \n{output}")
