# 필요한 라이브러리 임포트
import streamlit as st

# 선택형 입력 기능 구현 함수

## button() 함수
st.header("1. 버튼(button)")
if st.button("인사하기"):
    st.write("안녕하세요! 반가워요.")
else:
    st.write("버튼을 눌러보세요.")

## 구분선 생성 함수
st.divider()

## checkbox() 함수
st.header("2. 체크박스(checkbox)")
is_vip = st.checkbox("VIP 고객만 필터링하시겠습니까?")
st.write(f"반환된 값: {is_vip}")

## 구분선 생성 함수
st.divider()

## 파이썬 리스트 자료형 데이터 생성 -> 위젯으로 전달
customer_types = ["일반 고객", "VIP 고객", "기업 고객"]

## radio() 함수
st.header("3. 라디오 버튼(radio)")
selected_radio = st.radio("분석할 고객 유형을 하나만 고르세요: ", customer_types)
st.write(f"반환된 값: {selected_radio}")

## 구분선 생성 함수
st.divider()

## seltectbox() 함수
st.header("4. 셀렉트 박스(selectbox): 드롭다운 메뉴에서 하나만 선택")
selected_select = st.selectbox("조회할 고객 유형을 선택하세요: ", customer_types)
st.write(f"반환된 값: {selected_select}")

## 구분선 생성 함수
st.divider()

## multiselect() 함수
st.header("5. 멀티 셀렉트(multiselect): 드롭다운 메뉴에서 여러 개를 동시에 선택")
selected_multi = st.multiselect("원하는 고객 유형을 모두 고르세요", customer_types)
st.write(f"반환된 값: {selected_multi}")

## 구분선 생성 함수
st.divider()

## text_input 함수
st.header("6. 텍스트 입력(text_input)")
name = st.text_input("당신의 이름을 입력하세요")
### 값을 입력 받았을 때만 실행
if name:
    st.write(f"안녕하세요. {name}님!")

## number_input 함수
st.header("7. 숫자 입력(number_input)")
age = st.number_input("당신의 나이를 입력하세요", min_value=0, value=0, step=1)
### 값을 입력 받았을 때만 실행
if age:
    st.write(f"당신의 나이는 {age}세 입니다.")



