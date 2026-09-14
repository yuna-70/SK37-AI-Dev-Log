# 필요한 라이브러리 임포트
import streamlit as st

# 수치 카드 -> st.metric 함수
st.metric(label="오늘의 총 매출액", value="1,250,000", delta="15%")

# 구분선 생성
st.divider()

# 딕셔너리 데이터 기반 수평 막대 그래프 생성

## 딕셔너리 자료형 데이터 생성
monthly_sales = {"1월": 120, "2월": 180, "3월": 250, "4월": 210}
st.bar_chart(monthly_sales, horizontal=False)






