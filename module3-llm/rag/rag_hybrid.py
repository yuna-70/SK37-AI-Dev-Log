"""TIL: 하이브리드 검색(BM25 + 벡터) 기반 챗봇 (2026-11-18) — 개념 설명은 README.md 참고"""

import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from mecab import MeCab


# 1. 환경 설정
env_file_path = ".env"
output = load_dotenv(env_file_path)

print(output)


# 2. 데이터 로드 및 Document 자료형으로 변환
loader = TextLoader(file_path="tech_support_manual.txt", encoding="utf-8")

documents = loader.load()

print(f"documents: {documents}")


# 3. chunk_size를 정하기 위한 사전 계산
## 매뉴얼이 바뀌면 적절한 길이도 바뀌므로, 새 파일마다 다시 재서 근거를 만듦
file_path = "tech_support_manual.txt"

with open(file_path, "r", encoding="utf-8") as file:
    manual_text = file.read()

## 질문-답변 쌍이 문단("\n\n")으로 구분되어 있으므로 문단으로 나눔
qa_pairs = manual_text.split("\n\n")

print(qa_pairs)

## 각 질문-답변 쌍의 글자수 계산
character_length = []

for pair in qa_pairs:
    character_length.append(len(pair))

print(character_length)

## 가장 긴 QA 쌍의 글자수 -> chunk_size의 근거
max_char_length = max(character_length)

print(f"가장 긴 Q&A 단락의 글자 수: {max_char_length}자")

## 가장 긴 단락(208자)보다 조금 크게 설정
optimal_chunk_size = 210


# 4. 텍스트 분할
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=optimal_chunk_size,
    chunk_overlap=0,
)

docs = text_splitter.split_documents(documents)

print(f"분할된 문서 조각의 수: {len(docs)}")
print(f"분할된 문서 조각 예시: \n{docs[0]}")


# 5. MeCab 형태소 분석기 기반 토큰화 함수 정의
mecab = MeCab()


def mecab_tokenizer(text):
    ## 의미 있는 형태소(명사, 용언, 숫자, 영어 및 특수 기호 등) 추출 결과 저장용 빈 리스트 생성
    tokens = []

    ## 품사 태깅 -> [("형태소", "품사"), ...]
    tags = mecab.pos(text)

    for morph, pos in tags:
        if pos.startswith(("N", "V", "S")):
            tokens.append(morph)

    return tokens


# 6. BM25 희소 검색기 생성
## 키워드가 정확히 일치하는 문서를 찾음 -> 오류 코드, 모델명, 조항 번호에 강함
sparse_retriever = BM25Retriever.from_documents(
    documents=docs,
    preprocess_func=mecab_tokenizer,
    k=2,
)

## 희소 검색기 단독 테스트
test_query = "ERR-502 오류코드 조치법"
retrieved_docs = sparse_retriever.invoke(test_query)

for doc in retrieved_docs:
    print(f"내용: {doc.page_content}")
    print("-" * 80)


# 7. 임베딩 모델과 Chroma 밀집 검색기 생성
## 의미가 가까운 문서를 찾음 -> 표현이 달라도 뜻이 통하면 잡아냄
model_name = "text-embedding-3-small"
model = OpenAIEmbeddings(model=model_name)

chroma_path = "chroma_db_tech_support"

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

## 매개 변수 이름은 search_kwargs임. 철자가 틀리면 에러 없이 무시되고 k가 기본값 4로 동작함
dense_retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

print(f"밀집 검색 도구: {dense_retriever}")


# 8. EnsembleRetriever로 두 검색기 결합
## 여러 검색기의 결과를 하나로 통합하고, 가중치 기반 상호 순위 융합(RRF)으로 순위를 재조정함
## 매개 변수
##   retrievers: 결합할 검색기 리스트
##   weights: 각 검색기 결과에 부여할 가중치 리스트
## 두 검색기가 같은 문서를 찾으면 중복이 합쳐지므로 결과 개수는 합보다 적을 수 있음
hybrid_retriever = EnsembleRetriever(
    retrievers=[sparse_retriever, dense_retriever],
    weights=[0.5, 0.5],
)

print(f"하이브리드 검색 도구: {hybrid_retriever}")


# 9. 프롬프트 생성
system_prompt = """
당신은 스마트홈 IT 기기 및 지원 서비스의 전문 기술 지원 AI 엔지니어입니다.
제공된 [참고 컨텍스트] 정보를 바탕으로 고객의 제품 문의, 오류 코드 해결법, A/S 규정 질문에 정중하고 명확하게 답변해주세요.

[답변 작성 수칙]
1. [참고 컨텍스트]에 명시된 모델명, 오류 코드, 조치 단계, 규정 조항을 정확하게 인용하세요.
2. 답변을 시작할 때 '답변:'이라는 단어를 사용하지 마세요.
3. [참고 컨텍스트]에 고객 질문에 관한 내용이 없다면, "죄송합니다. 문의하신 내용에 대한 기술 매뉴얼 정보를 찾을 수 없습니다. 고객센터(1588-0000)로 문의 부탁드립니다."라고 답변하세요.

[참고 컨텍스트]
{context}
"""

user_prompt = "{question}"

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", user_prompt),
    ]
)

print(prompt)


# 10. LLM과 출력 파서 생성
llm = ChatOpenAI(model="gpt-5-nano")
output_parser = StrOutputParser()


# 11. RAG 체인 생성
rag_chain = prompt | llm | output_parser


# 12. 챗봇 실행
print("안녕하세요! 하이브리드 RAG 기반 고객 응대 챗봇입니다. 궁금한 점을 질문해주세요. (종료하려면 'exit' 입력)")
print("-" * 80)

while True:
    try:
        user_question = input("사용자 질문: ")

        ## 종료 조건
        if user_question.lower() == "exit":
            print("챗봇을 종료합니다. 이용해주셔서 감사합니다.")
            break

        ## 12-1. 하이브리드 검색 실행 -> RRF로 순위 재조정된 문서 리스트
        retrieved_docs = hybrid_retriever.invoke(user_question)
        print(f"하이브리드 검색 결과: 총 {len(retrieved_docs)}개 문서 수집")

        print("-" * 80)

        ## 12-2. 검색된 문서들의 텍스트를 하나의 문자열로 병합
        ### 추출한 텍스트를 담을 빈 리스트 생성
        contents = []

        ### 검색된 문서 리스트를 순회하며 텍스트(page_content) 추출
        for doc in retrieved_docs:
            text = doc.page_content
            contents.append(text)

        ### join()으로 "\n\n" 기준 연결
        context_text = "\n\n".join(contents)
        print(f"답변의 근거: \n{context_text}")

        print("-" * 80)

        ## 12-3. 생성
        response = rag_chain.invoke(
            {
                "context": context_text,
                "question": user_question,
            }
        )

        print(f"챗봇 응답: \n{response}")
        print("=" * 80)

    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
