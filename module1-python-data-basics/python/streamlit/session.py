# 필요한 라이브러리 임포트
import streamlit as st

# 안전한 초기화 (처음 웹을 실행할 때 1번만 실행)
if "count" not in st.session_state:
    ## 변수 생성 및 값 초기화: 0 입력
    st.session_state["count"] = 0

# 버튼을 누르면(조건 만족 시) 세션 상태 내부의 값을 1 증가
# button() 함수는 if 조건문과 함께 사용됨: 만일 버튼을 누르면, ~ 하겠다.
if st.button("숫자 1 증가"):
    st.session_state["count"] = st.session_state["count"] + 1

# 화면이 재실행되어도 변하지 않고 유지되는 값 출력
st.write(f"현재 누적 카운트: {st.session_state['count']}")



