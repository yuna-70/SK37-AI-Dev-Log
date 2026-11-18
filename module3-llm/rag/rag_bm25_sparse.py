"""TIL: BM25 키워드 기반 희소 검색 (2026-11-18) — 개념 설명은 README.md 참고"""

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.retrievers import BM25Retriever
from mecab import MeCab


# 1. 데이터 로드 및 Document 자료형으로 변환
loader = TextLoader(
    file_path="manual.txt",
    encoding="utf-8",
)

documents = loader.load()

print(f"documents: {documents}")


# 2. 텍스트 분할
## FAISS 실습에서 계산해둔 근거(가장 긴 QA 157자)를 그대로 사용
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=160,
    chunk_overlap=0,
)

docs = text_splitter.split_documents(documents)

print(f"분할된 문서 조각의 수: {len(docs)}")
print(f"분할된 문서 조각 예시: \n{docs[0]}")


# 3. MeCab 형태소 분석기 기반 토큰화 함수 정의
## BM25는 토큰이 정확히 일치해야 점수가 붙으므로, 조사와 어미를 떼어내야 함
## "환불은"과 "환불"이 다른 토큰으로 잡히면 검색이 실패함
mecab = MeCab()


def mecab_tokenizer(text):
    """
    Mecab 형태소 분석기를 사용하여 텍스트에서 의미 있는 형태소(명사, 용언, 숫자)만 추출합니다.
    - N: 명사 (NNG, NNP 등)
    - V: 용언 (VV: 동사, VA: 형용사 등)
    - S: 숫자 및 외국어, 기호 등 (SN, SL 등)
    """

    ## 의미 있는 형태소 추출 결과를 저장할 빈 리스트 생성
    tokens = []

    ## 품사 태깅 -> 결과: [("한글", "NNG"), ...]
    tags = mecab.pos(text)

    ## 튜플 언패킹으로 형태소와 품사를 각각 받음
    for morph, pos in tags:
        ### startswith()에 튜플을 넘기면 여러 접두사 중 하나라도 맞는지 한 번에 확인함
        if pos.startswith(("N", "V", "S")):
            tokens.append(morph)

    return tokens


## 참고: packing과 unpacking
## packing -> 데이터를 쉼표로 구분해 나열하면 tuple이 됨
data = "한글", "NNG"
print(data)

## unpacking -> 성분 원소의 개수만큼 변수를 지정해 한 번에 꺼냄
data1, data2 = data
print(data1)
print(data2)

## 참고: 문자열 전용 함수 startswith()
## 문자열이 특정 접두사로 시작하는지 불리언으로 반환하며, 매개 변수로 튜플을 받을 수 있음
text = "Hello, Python world!"
output = text.startswith(("Hi", "Hello", "Hey"))
print(output)


# 4. BM25 희소 검색기 생성
## BM25Retriever는 벡터 저장소를 거치지 않고 from_documents()로 바로 검색기를 만듦
## 매개 변수
##   documents: 분할된 문서 조각(Document의 리스트)
##   preprocess_func: 텍스트를 토큰 단위로 쪼개는 전처리 함수
##   k: 검색 시 반환할 상위 문서의 개수 (미지정 시 기본값 4)
## 생성 결과로 객체 안에 두 가지가 저장됨
##   docs: 검색 결과로 원본 문서를 돌려주기 위해 보관하는 Document 리스트
##   vectorizer: 문서별 단어 빈도, 단어별 idf, 문서 길이 등 점수 계산용 통계 자료
sparse_retriever = BM25Retriever.from_documents(
    documents=docs,
    preprocess_func=mecab_tokenizer,
    ## 연관성이 높은 문서 추출 조건 설정
    k=1,
)


# 5. BM25 검색기 성능 테스트
test_query = "환불 정책이 어떻게 되나요?"

retrieved_docs = sparse_retriever.invoke(test_query)

print(f"[Mecab 기반 BM25 희소 검색 결과]: \n{retrieved_docs}")

for doc in retrieved_docs:
    print(f"출처: {doc.metadata}")
    print(f"내용: {doc.page_content}")
