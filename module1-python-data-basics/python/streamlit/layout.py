# 필요한 라이브러리 임포트
import streamlit as st

# 사이드 바에 메뉴 배치

## 블록 지정(with 구문): with 구문 안쪽에 들여쓰기로 작성된 
## 모든 요소(텍스트, 위젯 등)은 메인 화면이 아닌 좌측 사이드바 내부에 배치
with st.sidebar:
    st.header("메뉴판")
    menu = st.radio("이동", ["홈", "상세보기"])

# 메인 화면 -> 가로로 균등하게 2개로(1:1) 분할
col1, col2 = st.columns(2)

## col1(왼쪽 화면) 구현: with 구문 -> "부착"의 의미
with col1:
    st.subheader("왼쪽 구역")
    with st.expander("원본 데이터"):
        monthly_sales = {"1월": 120, "2월": 180, "3월": 250, "4월": 210}
        st.write(monthly_sales)
## col2(오른쪽 화면) 구현: with 구문
with col2:
    st.subheader("오른쪽 구역")
    with st.expander("수평 막대 그래프"):
        st.bar_chart(data=monthly_sales, horizontal=False)

# 구분선 생성
st.divider()

# tab 생성 -> 반환된 객체를 각각 변수에 할당해서 화면 구현
tab1, tab2, tab3 = st.tabs(["차트 보기", "데이터 보기", "정보"])

## tab1 구현
with tab1:
    st.subheader("데이터 시각화")
    monthly_sales = {"1월": 120, "2월": 180, "3월": 250, "4월": 210}
    st.bar_chart(monthly_sales)

## tab2 구현
with tab2:
    st.subheader("원본 데이터")
    st.write(monthly_sales)

## tab3 구현
with tab3:
    st.write("이 앱은 st.tabs 함수를 활용하여 제작되었습니다.")
