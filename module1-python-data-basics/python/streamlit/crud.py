# 필요한 라이브러리 임포트
import streamlit as st

# 메모리(st.session_stats)에 고객 리스트 생성 및 초기화
if "customer_list" not in st.session_state:
    st.session_state["customer_list"] = []

# CRUD -> C(Creat): 데이터 추가
new_name = st.text_input("고객 이름 입력")

# if 조건문 -> 버튼 생성 -> 버튼을 누를 때마다 입력 받은 고객 이름을 추가
if st.button("고객 추가"):
    st.session_state["customer_list"].append({"name": new_name})
    # 작업이 문제없이 성공적으로 끝났음을 시각적으로 표시(알림 기능)
    st.success(f"{new_name} 고객이 등록되었습니다.")

# CRUD -> R -> 데이터 조회
st.write(f"현재 등록된 고객 목록: {st.session_state['customer_list']}")