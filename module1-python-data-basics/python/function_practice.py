"""TIL: 함수 종합 연습문제 (2026-09-09) — 개념 설명은 README.md 참고"""

# 문제 1
def multiply(x, y):
    output = x * y
    return output
output = multiply(4, 5)
print(output)

# 문제 2
def subtract(a, b):
    output = a - b
    return output
output = subtract(a=10, b=3)
print(output)

# 문제 3
def power(base, exponent):
    return base ** exponent
output = power(3, 3)
print(output)

# 문제 4
def concat_words(str1, str2):
    return str1 + " " + str2
output = concat_words("Hello", "World")
print(output)

# 문제 5
def get_greeting():
    return "파이썬 함수 단원 복습 시작!"
output = get_greeting()
print(output)

# 문제 6
text = "Python Programming"
print(text.upper())
print(text.lower())

# 문제 7
phrase = "data science"
print(phrase.capitalize())
print(phrase.title())

# 문제 8
raw_str = "\n Welcome to Python! \n"
output = raw_str.strip()
print(output)

# 문제 9
sentence = "I like Java"
output = sentence.replace("Java", "Python")
print(output)

# 문제 10
skill_str = "Python,SQL,R,Tableau"
output = skill_str.split(",")
print(output)

# 문제 11 — 하이픈 앞뒤 공백 포함하도록 수정 (" - ")
languages = ["Python", "Java", "C++"]
output = " - ".join(languages)
print(output)

# 문제 12
todo_list = []
todo_list.append("수업 듣기")
todo_list.append("복습하기")
print(len(todo_list))

# 문제 13
student = {"id": 202601, "name": "김민수", "dept": "컴퓨터공학과"}
print(student.keys())

# 문제 14
prices = {"사과": 1500, "바나나": 2000, "포도": 3000}
print(prices.values())

# 문제 15
profile = {"nickname": "Pythoner", "level": 5}
print(profile.items())

# 문제 16
user = {"username": "coder123"}
print(user.get("username"))
print(user.get("email"))

# 문제 17
def to_upper_sentence(text):
    output = text.upper()
    return f"변환된 문장: {output}"
output = to_upper_sentence("good morning")
print(output)

# 문제 18
# 시도1: + 연산자 -> 원본을 안 바꾸고 새 리스트를 만들어버림 (문제 요구사항과 다름)
# def add_and_count(lst, item):
#     new_list = lst + [item]
#     return len(new_list)

# 시도2(최종): append() -> 원본 리스트에 직접 아이템 추가
def add_and_count(lst, item):
    lst.append(item)
    length = len(lst)
    return length

my_list = [1, 2, 3]
output = add_and_count(my_list, 4)
print(output)

# 문제 19
def count_words(sentence):
    words = sentence.split()
    return len(words)
output = count_words("data analysis with python")
print(output)

# 문제 20
def get_info_msg(info, key_name):
    value = info.get(key_name)
    return f"요청하신 {key_name}의 정보는 {value}입니다."
person = {"name": "이영희", "age": 28}
output = get_info_msg(person, "name")
print(output)

# 문제 21 — strip() 결과에 이어서 replace()를 적용하도록 수정
def format_data(raw_data):
    output1 = raw_data.strip()
    output2 = output1.replace("-", "/")
    return output2

output = format_data("\n 2026-07-28 \n")
print(output)

# 문제 22
def count_values(dict_obj):
    value = dict_obj.values()
    return len(value)
menu = {"아메리카노": 3000, "라떼": 3500, "티": 4000}
output = count_values(menu)
print(output)

# 문제 23
def custom_join(words, sep):
    return sep.join(words)
first_list = ["apple", "banana", "orange"]
output = custom_join(first_list, ", ")
print(output)

# 문제 24
def get_quotient_remainder(num1, num2):
    output1 = num1 // num2
    output2 = num1 % num2
    return (output1, output2)
output = get_quotient_remainder(23, 5)
print(output)

# 문제 25
def summarize_dict(data_dict):
    keys = data_dict.keys()
    return f"등록된 항목은 총 {len(keys)}개입니다."
user_data = {"id": "user01", "name": "홍길동", "email": "hong@test.com"}
output = summarize_dict(user_data)
print(output)