"""TIL: Dictionary 생성 / 값 가져오기 / 추가·삭제·수정 (2026-09-07) — 개념 설명은 README.md 참고"""

# 딕셔너리 생성
dict_data1 = {}
print(dict_data1)

dict_data2 = {'name': '박보검'}
print(dict_data2)

dict_data3 = {1: '박보검', 2: '배우'}
print(dict_data3)

dict_data4 = {'name': ['박보검', '이찬원'], 'job': ['배우', '가수']}
print(dict_data4)

customer_info = {'name': 'MH', 'age': 20, 'phone': '010-1234-1234'}
print(customer_info)

# 값 가져오기
customer_name = customer_info['name']
print(f'고객의 이름 : {customer_name}')

customer_age = customer_info['age']
print(f'고객의 나이 : {customer_age}')

customer_phone = customer_info['phone']
print(f'고객의 전화 번호 : {customer_phone}')

# 데이터 추가
customer_info['birth'] = '03/27'
print(f'데이터 추가 후 결과 : {customer_info}')

# 참고: 리스트는 존재하지 않는 인덱스에 값을 대입할 수 없음(에러 발생)
list_data = [10, 20, 30, 40]
print(f'데이터 추가 전 리스트 자료형 데이터 : {list_data}')
# list_data[4] = 50  # IndexError 발생 (딕셔너리와 다른 점)

# 데이터 수정
customer_info['birth'] = '08/27'
print(f'데이터 수정 후 결과 : {customer_info}')