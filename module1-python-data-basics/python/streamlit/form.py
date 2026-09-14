# 필요한 라이브러리 임포트
import streamlit as st

# st.form()으로 입력 위젯들을 하나로 그룹화
# 여러 위젯을 묶을 때 -> with 사용
with st.form(key="user_info_form"):
    user_name = st.text_input("이름")
    user_age = st.text_input("나이 (숫자로만 입력)")

    # 양식 전송 전용 제출 버튼
    submit_btn = st.form_submit_button("제출하기")

# 제출 버튼이 눌렸을 때 실행 -> button click event 작성!!! -> if 조건문으로 작성
if submit_btn:
    try:
        # 문자열을 정수(int)로 변환 -> 문자열로 입력 시 ValueError 발생
        age_number = int(user_age)
        st.success(f"성공: {user_name}님의 나이는 {age_number}세로 확인되었습니다.")
    except ValueError:
        # 에러 발생 시 프로그램이 강제 종료되는 대신에 빨간색 안내창 표출
        st.error("경고: 나이 칸에는 반드시 숫자만 입렵하셔야 합니다!")

