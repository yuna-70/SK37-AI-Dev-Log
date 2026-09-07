"""TIL: Dictionary 연습문제 (2026-09-07) — 개념 설명은 README.md 참고"""

# 1. 나만의 인물 사전 만들기
my_star = {"name": "김성철", "job": "배우"}
print(my_star)

# 2. 딕셔너리 값 추출하여 문장 만들기
my_city = {'city': '서울', 'population': 940}
location = my_city['city']
number = my_city['population']
print(f"제가 사는 곳은 {location}이고, 인구는 {number}만 명입니다.")

# 3. 새로운 정보 추가하기
product = {'name': '커피', 'price': 5000}
product['stock'] = 100
print(f'추가 후 딕셔너리 : {product}')

# 4. 기존 정보 수정하기
product['price'] = 5500
print(f'가격 인상 후 딕셔너리 : {product}')

# 5. 리스트를 값으로 갖는 딕셔너리 만들기
movie = {"title": "파이썬", "actors": ["배우1", "배우2"]}
print(f"영화 정보 : {movie}")

# 데이터 추가/삭제 실습 (dict_test)
dict_test = {"노래제목": "아무노래"}
print(f"데이터 추가 전 딕셔너리 : {dict_test}")

dict_test["가수"] = "지코"
print(f"데이터 추가 후 딕셔너리 : {dict_test}")

dict_test["날짜"] = "2020.01.13"
print(f"데이터 추가 후 딕셔너리 : {dict_test}")

del dict_test["날짜"]
print(f"데이터 삭제 후 딕셔너리 : {dict_test}")