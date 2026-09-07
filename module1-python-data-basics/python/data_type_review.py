"""TIL: 자료형 종합 복습 25문제 (2026-09-07) — 개념 설명은 README.md 참고"""

# 문제 1
# 변수와 f-string을 이용한 출력 변수 name에 '홍길동', age에 25를 저장한 후, 
# f-string 접두사를 사용하여 "제 이름은 홍길동이고, 나이는 25세입니다." 형식으로 문장을 출력하는 코드를 작성하세요.
name = "홍길동"
age = 25
print(f"제 이름은 {name}이고, 나이는 {age}세입니다.")

# 문제 2
# 숫자형 사칙 연산 변수 num1에 15, num2에 4를 할당하고, 
# 두 수의 덧셈, 뺄셈, 곱셈, 나눗셈 결과를 각각 출력하는 코드를 작성하세요.
num1 = 15
num2 = 4
total = num1 + num2
sub = num1 - num2
mul = num1 * num2
div = num1 / num2
print(f"덧셈 : {total}")
print(f"뺄셈 : {sub}")
print(f"곱셈 : {mul}")
print(f"나눗셈 : {div}")

# 문제 3
# 제곱 연산자(**) 활용 변수 base에 2, exponent에 10을 저장한 뒤, 
# 제곱 연산자(**)를 사용하여 2의 10제곱 값을 계산하여 출력하는 코드를 작성하세요.
base = 2
exponent = 10
print(f"2의 10제곱 : {base ** exponent}")

# 문제 4
# 몫(//)과 나머지(%) 연산자 17을 5로 나누었을 때의 몫과 나머지를 
# 각각 몫 연산자(//)와 나머지 연산자(%)를 이용해 구하고 출력하는 코드를 작성하세요.
quo = 17 // 5
rem = 17 % 5
print(f"몫 : {quo}, 나머지 : {rem}")

# 문제 5
# 불리언 수치 연산 특성 불리언 값 bool_data1 = True, bool_data2 = False를 생성하고, 
# 두값을 덧셈 연산(bool_data1 + bool_data1 + bool_data2)한 결과를 출력하는 코드를 작성하세요.
bool_data1 = True
bool_data2 = False
total = bool_data1 + bool_data1 + bool_data2
print(f"덧셈 결과 : {total}")

# 문제 6
# 여러 줄 문자열 생성과 길이 측정 작은따옴표 3개(''')를 사용하여 3줄 이상의 임의의 문자열 변수 multi_str을 생성하고, 
# len() 함수를 사용해 전체 글자 수를 출력하는 코드를 작성하세요.
multi_str = """
Test1
Test2
Test3
"""
print(f"전체 글자 수 : {len(multi_str)}")

# 문제 7
# 문자열 인덱싱 문자열 text = "파이썬프로그래밍"에서 인덱싱을 통해 
# 첫 번째 글자인 '파'와 마지막 글자인 '밍'을 각각 추출하여 출력하는 코드를 작성하세요.
text = "파이썬프로그래밍"
print(f"첫 번째 글자 : {text[0]}, 마지막 글자 : {text[-1]}")

# 문제 8
# 문자열 슬라이싱 문자열 string = "문자열은 인덱싱과 슬라이싱이 가능하다"에서
#  슬라이싱을 활용하여 "인덱싱과 슬라이싱" 부분만 추출하여 출력하는 코드를 작성하세요.
string = "문자열은 인덱싱과 슬라이싱이 가능하다"
sliced_str = string[5:14]
print(f"슬라이싱 한 문자열 : {sliced_str}")

# 문제 9
# 문자열 연결과 반복 str1 = "Python", str2 = " ", str3 = "Fun"을 덧셈 연산자로 연결하여 
# "Python Fun"을 출력하고, 곱셈 연산자를 사용하여 "=" 문자를 20번 반복한 구분선을 출력하는 코드를 작성하세요.
str1, str2, str3 = "Python", " ", "Fun"
print(str1 + str2 + str3)
print("=" * 20)

# 문제 10
# 리스트 기본 인덱싱 numbers = [10, 20, 30, 40, 50] 리스트에서 
# 세 번째 원소(30)와 다섯 번째 원소(50)를 인덱싱하여 두 수의 합을 출력하는 코드를 작성하세요.
numbers = [10, 20, 30, 40, 50]
total = numbers[2] + numbers[4]
print(f"두 수의 합 : {total}")

# 문제 11
# 중첩 리스트 인덱싱 리스트 nested_list = [1, 2, 3, ['a', 'b', 'c']]에서 
# 문자 'b'만 인덱싱으로 추출하여 출력하는 코드를 작성하세요.
nested_list = [1, 2, 3, ['a', 'b', 'c']]
print(f"문자 b : {nested_list[3][1]}")

# 문제 12
# 리스트 슬라이싱 data_list = [0, 10, 20, 30, 40, 50]에서 
# [20, 30, 40] 부분 리스트만 슬라이싱하여 출력하는 코드를 작성하세요.
data_list = [0, 10, 20, 30, 40, 50]
sliced_list = data_list[2:5]
print(f"슬라이싱 한 부분 : {sliced_list}")

# 문제 13
# 튜플 생성 및 인덱싱 원소 1, 2, 3을 갖는 튜플 t = (1, 2, 3)을 생성하고 첫 번째 원소를 출력하는 코드를 작성하세요.
my_tuple = (1, 2, 3)
print(f"첫 번째 원소 : {my_tuple[0]}")

# 문제 14
# 딕셔너리 생성 및 값 추출 Key가 'title', Value가 '파이썬', Key가 'year', Value가 2026인 딕셔너리 movie를 생성하고, 
# Key가 'title'인 Value를 추출하여 출력하는 코드를 작성하세요.
movie = {"title": "파이썬", "year": 2026}
print(f"딕셔너리 값 : {movie['title']}")

# 문제 15
# 딕셔너리 데이터 추가 및 수정 빈 딕셔너리 user_info = {}를 만든 후, Key: 'name', Value: 'Alice' 데이터를 추가하고, 
# Key: 'name'의 Value를 'Bob'으로 수정한 뒤 최종 딕셔너리를 출력하는 코드를 작성하세요.
user_info = {}
user_info["name"] = "Alice"
user_info["name"] = "Bob"
print(f"최종 딕셔너리 : {user_info}")

# 문제 16
# 딕셔너리와 리스트 인덱싱 융합 person = {'name': 'MH', 'hobbies': ['코딩', '독서', '운동']} 딕셔너리에서 
# 이름과 두 번째 취미('독서')를 각각 추출하여 f-string으로 "MH의 두 번째 취미는 독서입니다." 형식으로 출력하는 코드를 작성하세요.
person = {"name": "MH", "hobbies": ["코딩", "독서", "운동"]}
name = person["name"]
hobby = person["hobbies"][1]
print(f"{name}의 두 번째 취미는 {hobby}입니다.")

# 문제 17
# 리스트와 산술 연산자 융합 scores = [85, 92, 78] 리스트의 세 원소를 모두 더한 합계를 구하고, 
# 3으로 나눈 몫(//)을 이용해 평균 점수(정수)를 구하여 합계와 평균 몫을 각각 출력하는 코드를 작성하세요.
scores = [85, 92, 78]
total = scores[0] + scores[1] + scores[2]
avg = int(total // 3)
print(f"합계 : {total}, 평균 몫 : {avg}")

# 문제 18
# 불리언 크기 비교와 딕셔너리 저장 융합 변수 my_money = 15000이 10000보다 큰지 크기 비교한 불리언 결과를 구하여, 
# result_dict = {}의 Key 'is_rich'의 Value로 저장한 후 딕셔너리를 출력하는 코드를 작성하세요.
my_money = 15000
is_rich = my_money > 10000
result_dict = {}
result_dict["is_rich"] = is_rich
print(f"딕셔너리 : {result_dict}")

# 문제 19
# 문자열 슬라이싱과 리스트 융합 주민등록번호 문자열 pin = "990101-1234567"에서 생년월일 앞 6자리("990101")와 뒤 7자리("1234567")를 슬라이싱하여 추출하고, 
# 두 문자열을 원소로 갖는 리스트 pin_list를 만들어 출력하는 코드를 작성하세요.
pin = "990101-1234567"
birth = pin[0:6]
code = pin[7:14]
pin_list = [birth, code]
print(f"리스트 : {pin_list}")

# 문제 20
# 튜플 인덱싱과 제곱 연산자 융합 튜플 dimensions = (3, 4, 5)의 첫 번째 원소(3)의 2제곱과 두 번째 원소(4)의 2제곱의 합을 계산하고, 
# f-string을 이용하여 "계산 결과: 25" 형식으로 출력하는 코드를 작성하세요.
dimensions = (3, 4, 5)
result = (dimensions[0] ** 2) + (dimensions[1] ** 2)
print(f"계산 결과 : {result}")

# 문제 21
# 딕셔너리 수정과 나머지 연산자 융합 딕셔너리 item = {'count': 11}의 'count' 값을 12로 수정하고, 
# 수정된 count 값을 2로 나눈 나머지(%)를 구하여 출력하는 코드를 작성하세요.
item = {"count": 11}
item["count"] = 12
rem = item["count"] % 2
print(f"나머지 : {rem}")

# 문제 22
# 중첩 리스트와 문자열 슬라이싱 융합 리스트 complex_data = [100, ["Python_Basic", "Data_Analysis"]]에서 
# 인덱싱으로 "Python_Basic"을 찾아낸 후, 슬라이싱을 사용하여 "Python" 단어만 추출하여 출력하는 코드를 작성하세요.
complex_data = [100, ["Python_Basic", "Data_Analysis"]]
target = complex_data[1][0]
sliced_word = target[:6]
print(f"단어 : {sliced_word}")

# 문제 23
# 불리언 연산과 문자열 곱셈 융합 불리언 변수 b1 = True, b2 = True, b3 = False의 합산 결과를 계산하여 반복 횟수로 사용하고, 
# 문자열 "*"를 해당 횟수만큼 곱하여 출력하는 코드를 작성하세요.
b1, b2, b3 = True, True, False
count = b1 + b2 + b3
print("*" * count)

# 문제 24
# 리스트와 딕셔너리 구조화 융합 이름 리스트 names = ['박보검', '이찬원']과 직업 리스트 jobs = ['배우', '가수']를 활용하여 
# {'name': names, 'job': jobs} 형태의 딕셔너리 data를 생성하고 출력하는 코드를 작성하세요.
names = ["박보검", "이찬원"]
jobs = ["배우", "가수"]
data = {"name": names, "job": jobs}
print(f"결과 : {data}")

# 문제 25
# 튜플과 리스트 비교 응용 튜플 tuple_data = (10, 20, 30) 대신 동일한 원소 [10, 20, 30]를 갖는 리스트 list_data를 생성하고, 
# 첫 번째 원소를 100으로 변경한 후 리스트를 출력하는 코드를 작성하세요 (튜플은 원소를 수정할 수 없음을 주석으로 작성하세요).

# 튜플은 원소를 수정할 수 없으므로 리스트를 새로 생성하여 수정함
tuple_data = (10, 20, 30)
# tuple_data[0] = 100  # TypeError 발생
list_data = [10, 20, 30]
list_data[0] = 100
print(f"리스트 출력 : {list_data}")