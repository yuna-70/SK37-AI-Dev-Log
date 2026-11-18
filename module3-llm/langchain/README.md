# Module 3 - LangChain (Chain / 챗봇 / 에이전트)

## 📅 2026-11-13 | LangChain으로 체인과 에이전트 만들기

> 코드: [`chain_basics.py`](./chain_basics.py)
> 코드: [`langchain_chatbot.py`](./langchain_chatbot.py)
> 코드: [`search_agent.py`](./search_agent.py)

### 개념

**1. LangChain과 chain**

- LangChain은 LLM 애플리케이션을 만들기 위한 프레임워크임. 프롬프트, 모델, 출력 처리를 각각 독립된 조각으로 만들고 이어 붙이는 방식으로 작업함
- chain은 그 조각들을 순서대로 연결한 하나의 실행 단위임. 연결에는 `|` 기호를 쓰고, 이 방식을 LCEL(LangChain Expression Language)이라고 부름
- 전날 OpenAI API를 직접 쓸 때는 `get_completion()` 같은 함수를 만들어 호출을 감쌌는데, chain이 그 역할을 대신함

**2. chain의 세 가지 구성 요소**

- **프롬프트**: `ChatPromptTemplate.from_messages()`로 시스템 프롬프트와 사용자 프롬프트를 한 번에 작성함. `{topic}`처럼 중괄호로 변수 자리를 비워둘 수 있음
- **LLM 모델**: `ChatOpenAI(model="gpt-5-nano")`로 생성함. 이 자리만 갈아끼우면 다른 모델로 바꿀 수 있음
- **출력 도구**: `StrOutputParser()`가 LLM 응답 객체에서 텍스트만 꺼내줌. 이게 없으면 메타데이터가 잔뜩 붙은 객체가 그대로 나옴
- 세 개를 `chain = prompt | llm | output_parser`로 잇고, `chain.invoke({"topic": "양자 컴퓨터"})`처럼 딕셔너리로 변수 값을 채워 실행함

**3. 대화를 기억하는 챗봇**

- LLM은 호출 사이에 아무것도 기억하지 못함. 연속된 대화처럼 보이게 하려면 **이전 대화를 매번 통째로 다시 보내야** 함
- `MessagesPlaceholder(variable_name="chat_history")`가 프롬프트 안에 그 이력이 들어갈 자리를 비워두는 역할을 함
- 사용자 입력은 `HumanMessage`, LLM 답변은 `AIMessage`로 감싸 `chat_history` 리스트에 쌓음. 문자열 그대로 넣지 않고 감싸는 이유는 누가 한 말인지 역할을 표시해야 하기 때문임
- 대화가 길어질수록 보내는 프롬프트도 길어지고, 토큰은 길이만큼 과금되므로 비용도 함께 늘어남

**4. 도구(Tool)**

- 도구는 LLM이 자기가 할 수 없는 일을 대신 해주는 외부 기능임. `TavilySearch`는 실시간 웹 검색을 담당함
- 도구는 `name`과 `description`을 갖고 있음. 이 중 **설명이 특히 중요**한데, 에이전트가 이 글을 읽고 "언제 이 도구를 써야 하는지"를 판단하기 때문임
- 도구만 따로 쓸 수도 있음. 그럴 때는 `search_tool.invoke(query)`처럼 검색어를 사람이 직접 만들어 넣어야 함

**5. Agent와 ReAct**

- 에이전트는 도구를 **쓸지 말지, 무엇으로 검색할지 스스로 판단**하는 LLM임
- `create_agent(model, tools, system_prompt)`로 만들며, 동작 방식은 ReAct(Reasoning + Acting)임. 판단 → 도구 실행 → 결과 관찰 → 다시 판단을 답이 나올 때까지 자동으로 반복함
- 실행 결과의 `messages` 리스트에는 중간 과정이 모두 쌓이므로, 최종 답변은 `response["messages"][-1].content`로 꺼냄

### 왜 이렇게 코딩했는가

- 프롬프트에 `{topic}`, `{review}` 같은 변수를 비워둔 이유는 **같은 chain을 입력만 바꿔 계속 쓰기 위함**임. 질문이 바뀔 때마다 프롬프트를 새로 쓰지 않아도 됨
- 감성 분석 chain을 만들 때 프롬프트만 새로 작성하고 `llm`과 `output_parser`는 앞에서 만든 것을 그대로 썼음. chain을 조각으로 나눠둔 덕분에 바뀌는 부분만 교체할 수 있음
- `StrOutputParser()`를 붙인 이유는 chain의 결과를 바로 `print()`하거나 다른 함수에 넘기기 위함임. 붙이지 않으면 응답 객체가 나와서 `.content`를 또 꺼내야 함
- 챗봇에서 `chat_history.append()`를 **chain 호출 전후로 두 번** 하는 이유는, 호출 전에는 사용자 질문을 넣어야 LLM이 그걸 보고 답하고, 호출 후에는 LLM의 답변을 넣어야 다음 턴에서 기억되기 때문임
- 에이전트의 시스템 프롬프트에 "검색 결과에 기반하여 환각 없이"라고 쓴 이유는, 도구를 줬어도 LLM이 자기가 알던 내용으로 답해버릴 수 있기 때문임. 도구를 붙이는 것과 도구 결과를 쓰게 하는 건 다른 문제임
- 에이전트 쪽 `TavilySearch`에만 `search_depth="advanced"`를 준 것은, 에이전트가 다루는 질문이 더 포괄적이어서 검색을 깊게 할 필요가 있기 때문임

### 이해 포인트

- **전날 직접 만들었던 것이 그대로 구성 요소가 되어 있었음**
  - 11월 12일에는 시스템·사용자 프롬프트를 `messages` 리스트로 직접 만들고, `client.chat.completions.create()`를 호출하고, `response.choices[0].message.content`로 텍스트를 꺼냈음
  - LangChain에서는 이 세 단계가 각각 `ChatPromptTemplate`, `ChatOpenAI`, `StrOutputParser`로 나뉘어 있었음
  - 같은 일을 하는데 이름이 붙고 자리가 나뉘니까, 바꾸고 싶은 부분만 갈아끼울 수 있게 됐음
- **같은 감성 분석 과제를 한 주에 세 가지 방법으로 풀었음**
  - 화요일 HuggingFace `pipeline`: 결과가 `{'label': 'LABEL_1', 'score': 0.99}`로 판단 근거는 알 수 없었음
  - 목요일 OpenAI API: 프롬프트로 출력 형식을 지정해 키워드와 판단 이유까지 받았음
  - 금요일 LangChain chain: 같은 일을 하되 프롬프트·모델·출력이 분리되어 재사용할 수 있는 형태가 됐음
  - 코드는 점점 짧아지는데 결과는 점점 풍부해졌음
- **수요일 챗봇과 금요일 챗봇은 기억하는 방식이 완전히 달랐음**
  - 수요일 유사도 챗봇은 질문 하나를 받아 미리 준비된 11,823개 중 가장 비슷한 것을 찾아 그 답을 돌려주는 구조였음. 앞의 대화와 무관하게 매번 처음부터 시작했음
  - 금요일 챗봇은 대화 전체를 리스트에 쌓아 매 호출마다 다시 보냄. 기억이란 게 모델 안에 저장되는 게 아니라 **매번 다시 읽히는 것**이라는 걸 알게 됐음
  - 그래서 대화가 길어질수록 매 턴의 비용이 늘어난다는 것도 같이 보였음
- **도구의 `description`이 코드가 아니라 글이라는 점이 낯설었음**
  - `search_tool.description`을 출력해보니 "현재 사건에 대한 질문에 답해야 할 때 유용하다"는 식의 영어 설명문이 나왔음
  - 에이전트는 이 문장을 읽고 도구를 쓸지 판단함. 즉 도구를 잘 만들려면 **설명을 잘 쓰는 것**이 기능을 잘 구현하는 것만큼 중요함
- **목요일 웹 검색과 금요일 에이전트의 차이가 분명했음**
  - 목요일 Responses API의 `web_search_preview`는 OpenAI가 제공하는 붙박이 기능이었음
  - 금요일 에이전트는 도구를 목록으로 만들어 건네주는 방식이라, 다른 도구로 바꾸거나 여러 개를 함께 줄 수 있음
  - 에이전트가 도구를 쓸지 말지 스스로 정한다는 점도 달랐음

---
