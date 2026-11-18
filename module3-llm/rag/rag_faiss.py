"""TIL: FAISS 벡터 저장소로 만든 문서 기반 챗봇 (2026-11-16 ~ 11-17) — 개념 설명은 README.md 참고"""

from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# 1. 환경 설정
env_file_path = ".env"
output = load_dotenv(env_file_path)

print(output)


# 2. 데이터 로드 및 Document 자료형으로 변환
## TextLoader: .txt 파일에서 텍스트를 추출하고 LangChain의 기본 자료형인 Document로 변환
## Document = metadata(파일 경로 등) + page_content(텍스트 내용)
## .txt 파일 1개당 Document 1개가 생성됨
txt_file_path = "manual.txt"
loader = TextLoader(file_path=txt_file_path, encoding="utf-8")

documents = loader.load()

print(f"데이터 로드 및 변환의 결과물: \n{documents}")


# 3. chunk_size를 정하기 위한 사전 계산
## 분할 기준을 감으로 정하지 않고, 실제 데이터의 길이를 재서 근거를 만듦
with open(txt_file_path, "r", encoding="utf-8") as f:
    manual_text = f.read()

## 3-1. 질문-답변 쌍이 문단 단위('\n\n')로 구분되어 있으므로 문단으로 나눔
qa_pairs = []

for pair in manual_text.split("\n\n"):
    qa_pairs.append(pair)

## 3-2. 각 QA 쌍의 글자수 계산
character_length = []

for pair in qa_pairs:
    character_length.append(len(pair))

print(f"각 질문-답변 쌍의 글자수: \n{character_length}")

## 3-3. 가장 긴 QA 쌍의 글자수 -> chunk_size의 근거
max_char_length = max(character_length)

print(f"가장 긴 QA 단락의 글자 수: {max_char_length}자")


# 4. 데이터 분할
## RecursiveCharacterTextSplitter: 큰 단위부터 순서대로 쪼개는 분할 도구
## 분할 순서: "\n\n"(단락) -> "\n"(문장) -> " "(공백) -> ""(글자)
## chunk_size보다 크면 다음 구분자로 다시 쪼개고, 짧으면 병합
## chunk_overlap: 인접한 청크 간 중복 문자 수. QA나 법률 문서는 0, 일반 소설은 chunk_size의 10% 정도
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=160,
    chunk_overlap=0,
)

docs = text_splitter.split_documents(documents=documents)

print(f"분할된 문서의 수: {len(docs)}")
print(f"분할된 첫 번째 문서: \n{docs[0]}")


# 5. 임베딩 모델 생성
## 텍스트를 벡터로 바꿔주는 모델. 저장할 때와 검색할 때 같은 모델을 써야 함
model_name = "text-embedding-3-small"
model = OpenAIEmbeddings(model=model_name)


# 6. 벡터 저장소 생성
## FAISS.from_documents(): 각 Document의 텍스트를 임베딩해 메모리에 저장
## FAISS 내부 구조
##   index: 임베딩 벡터 배열만 저장
##   docstore: 원본 텍스트(page_content)와 메타데이터 저장
vectorstore = FAISS.from_documents(docs, model)

print(vectorstore.index)
print(vectorstore.docstore)


# 7. 검색 도구 생성
## as_retriever(): 사용자 질문과 가장 유사한 텍스트를 찾아주는 도구
## search_kwargs={'k': n} -> 유사도가 가장 높은 n개를 가져옴
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

print(f"검색 도구: {retriever}")

## 검색 도구 단독 테스트
user_query = "환불 가능한가요?"
output = retriever.invoke(user_query)

print(f"검색 결과: \n{output}")


# 8. 프롬프트 생성
## {context}에 검색된 문서를, {question}에 사용자 질문을 넣음
## 3번 규칙이 핵심: 검색 도구는 관련이 없어도 가장 가까운 문서를 돌려주므로,
## 근거가 없을 때 모른다고 답하게 하는 장치가 필요함
system_prompt = """
당신은 친절한 온라인 교육 플랫폼 직원입니다.
제공된 [컨텍스트]를 바탕으로 고객의 질문에 정중하게 답변해주세요.

[답변 규칙]
1. [컨텍스트]의 내용을 바탕으로 자연스럽게 답변을 재구성하거나 그대로 활용하세요.
2. 답변 시 '답변:'이라는 표현을 사용하지 마세요.
3. [컨텍스트]에 질문에 대한 정보가 없다면, '죄송하지만 문의하신 내용에 대해서는 아는 바가 없습니다.'라고 답변하세요.

[컨텍스트]
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


# 9. LLM과 출력 파서 생성
llm = ChatOpenAI(model="gpt-5-nano")
output_parser = StrOutputParser()


# 10. RAG 체인 생성
## 검색은 체인 밖에서 따로 하고, 그 결과를 context로 넣어주는 구조
rag_chain = prompt | llm | output_parser


# 11. 챗봇 실행
print("안녕하세요! 고객 응대 챗봇입니다. 궁금한 점을 질문해주세요. (종료하려면 'exit' 입력)")

while True:
    try:
        user_query = input("질문: ")

        ## 종료 조건
        if user_query.lower() == "exit":
            print("챗봇을 종료합니다. 이용해주셔서 감사합니다.")
            break

        ## 11-1. 검색: 사용자 질문과 가장 유사한 Document 리스트 생성
        retrieved_docs = retriever.invoke(user_query)
        print(f"사용자 질문과 가장 유사한 문서 리스트: \n{retrieved_docs}")

        ## 11-2. 검색된 문서에서 텍스트만 추출 -> 답변의 근거
        context_text = retrieved_docs[0].page_content
        print(f"답변의 근거: \n{context_text}")

        print("-" * 80)

        ## 11-3. 생성: 근거와 질문을 함께 넣어 답변 생성
        response = rag_chain.invoke(
            {
                "context": context_text,
                "question": user_query,
            }
        )
        print(f"chatbot 응답: \n{response}")

        print("-" * 80)

    except Exception as e:
        print(f"오류가 발생합니다.: {e}")
