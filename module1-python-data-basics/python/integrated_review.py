"""TIL: 자료형/함수/제어문 통합 복습 16문제 (2026-09-10) — 개념 설명은 README.md 참고"""

# 문제 1
# [리스트 + for 반복문 + if-else 조건문 + 나머지 연산자 % 융합] 숫자 리스트
# numbers = [12, 7, 19, 24, 30, 15]가 있습니다. for문과 나머지 연산자(%)를 사용하여 짝수는 evens 리스트에,
# 홀수는 odds 리스트에 각각 .append()로 분류해 저장하고 두 리스트를 출력하는 코드를 작성하세요.
numbers = [12, 7, 19, 24, 30, 15]
evens = []
odds = []

for num in numbers:
    if num % 2 == 0:
        evens.append(num)
    else:
        odds.append(num)

print(f"evens: {evens}, odds: {odds}")

# 문제 2
# [사용자 정의 함수 + 문자열 .strip() + f-string 융합] 고객 이름(name)과 양쪽에 공백 및
# 줄바꿈이 들어간 전화번호(phone)를 매개변수로 받는 함수 format_customer_info를 정의하세요.
# 함수 내부에서 전화번호의 양쪽 공백을 .strip()으로 제거하고, f-string을 활용해
# "고객 [name]님의 연락처는 [phone]입니다." 형식으로 반환하는 코드를 작성하세요.
def format_customer_info(name, phone):
    cleaned_phone = phone.strip()
    return f"고객 {name}님의 연락처는 {cleaned_phone}입니다."

output = format_customer_info("yuna", " 010-1234-5678 \n")
print(output)

# 문제 3
# [리스트 + for 반복문 + 문자열 슬라이싱 + if 조건문 융합] 파일 이름들이 담긴 리스트
# files = ["report.pdf", "data.csv", "image.png", "result.csv"]가 있습니다. for 반복문과 문자열
# 슬라이싱([-4:])을 사용하여 파일 확장자가 ".csv"인 파일명만 추출하여 csv_files 리스트에 추가하고 출력하는 코드를 작성하세요.
files = ["report.pdf", "data.csv", "image.png", "result.csv"]
csv_files = []

for file_name in files:
    if file_name[-4:] == ".csv":
        csv_files.append(file_name)

print(csv_files)

# 문제 4
# [사용자 정의 함수 + 딕셔너리 .items() + if-else + 산술 연산자 융합] 상품명과 가격이 담긴
# 딕셔너리(price_dict)와 할인율(discount_rate)을 매개변수로 받는 함수 apply_discount를 정의하세요.
# 가격이 10000원 이상인 상품만 할인율을 적용하여 정수(int) 할인가로 계산하고,
# 10000원 미만인 상품은 기존 가격 그대로 유지하여 새로운 딕셔너리로 반환하는 코드를 작성하세요.
def apply_discount(price_dict, discount_rate):
    new_prices = {}
    for name, price in price_dict.items():
        if price >= 10000:
            discounted_price = price * (1 - discount_rate)
            discounted_price_int = int(discounted_price)
            new_prices[name] = discounted_price_int
        else:
            new_prices[name] = price
    return new_prices

menu = {"커피": 4000, "원두 세트": 20000, "텀블러": 15000}
output = apply_discount(menu, 0.2)
print(output)

# 문제 5
# [사용자 정의 함수 + 문자열 .strip() + .title() 융합] 공백이 포함된 소문자 이름
# 문자열(raw_name)을 매개변수로 받는 함수 clean_and_title을 정의하세요.
# 양쪽 공백을 제거(.strip())한 뒤, 각 단어의 첫 글자를 대문자로 변환(.title())하여 반환하는 코드를 작성하세요.
def clean_and_title(raw_name):
    output1 = raw_name.strip()
    output2 = output1.title()
    return output2

output = clean_and_title("python py th on")
print(output)

# 문제 6
# [사용자 정의 함수 + for 반복문 + 문자열 len() + 리스트 .append() 융합] 단어
# 리스트(word_list)와 최소 길이(min_len)를 매개변수로 받아서, 단어의 길이(len())가 min_len
# 이상인 단어만 모아서 새 리스트로 반환하는 함수 filter_long_words를 정의하고 호출하는 코드를 작성하세요.
def filter_long_words(word_list, min_len):
    result = []
    for word in word_list:
        if len(word) >= min_len:
            result.append(word)
    return result

output = filter_long_words(["adfas", "ddddf", "sssd", "sfdsfs", "aafs"], 5)
print(output)

# 문제 7
# [딕셔너리 .get() + if-else 조건문 융합] 사용자 정보 딕셔너리 user = {"name": "Alice", "role": "admin", "active": True}가 있습니다.
# .get("active") 함수로 계정 활성화 여부를 안전하게 가져와서,
# 그 값이 True이면 "접근 허용", 그렇지 않으면 "접근 거부"를 출력하는 코드를 작성하세요.
user = {"name": "Alice", "role": "admin", "active": True}

if user.get("active") == True:
    print("접근 허용")
else:
    print("접근 거부")

# 문제 8
# [for 반복문 + range() + 나머지 연산자 % + 누적 합산 융합] range(1, 21)과 for 반복문을 사용하여
# 1부터 20까지의 정수 중 3의 배수(% 3 == 0)에 해당하는 수들의 합을 구하여 출력하는 코드를 작성하세요.
total = 0

for number in range(1, 21):
    if number % 3 == 0:
        total += number

print(total)

# 문제 9
# [사용자 정의 함수 + 문자열 .strip() + .split() 융합] 양쪽 공백이 들어간 쉼표 구분
# 문자열(raw_text)을 입력받아, 양쪽 공백을 제거(.strip())한 후 쉼표(,) 기준으로 분리(.split(","))된
# 리스트를 반환하는 함수 parse_str_to_list를 작성하고 호출 결과를 출력하세요.
def parse_str_to_list(raw_text):
    output1 = raw_text.strip()
    output2 = output1.split(",")
    return output2

output = parse_str_to_list(" python,java,c,c++,c# ")
print(output)

# 문제 10
# [while True 무한 루프 + 카운터 연산 + if 조건문 + break 융합] 로그인 시도 횟수 측정하는
# 변수 attempts = 0을 설정하세요. while True: 무한 루프 내에서 반복할 때마다
# attempts를 1씩 증가시키고 "로그인 시도 횟수: [attempts]"를 출력하세요. 시도 횟수가 3이 되면
# "비밀번호 3회 오류: 계정이 잠깁니다."를 출력하고 break로 루프를 탈출하는 코드를 작성하세요.
attempts = 0

while True:
    print(f"로그인 시도 횟수:{attempts}")
    if attempts == 3:
        print("비밀번호 3회 오류: 계정이 잠깁니다.")
        break
    attempts += 1

# 문제 11
# [사용자 정의 함수 + 딕셔너리 .get() + 리스트 인덱싱 + 몫 연산자 // + if-else 융합] 학생
# 정보 딕셔너리(student_info = {"name": "김철수", "scores": [90, 85, 80]})를 매개변수로 받는 함수
# check_student_pass를 정의하세요. 함수 내부에서 점수 리스트의 3개 과목 합을 구하고 3으로
# 나눈 몫(//)으로 평균 정수를 구하세요. 평균이 80점 이상이면 "[name]님 합격 (평균: [avg]점)",
# 그렇지 않으면 "[name]님 불합격 (평균: [avg]점)" 문자열을 반환하는 코드를 작성하세요.
student_info = {"name": "김철수", "scores": [90, 85, 80]}

def check_student_pass(student_info):
    total = 0
    for score in student_info.get("scores"):
        total += score
    avg = total // 3
    if avg >= 80:
        return f"{student_info.get('name')}님 합격 (평균: {avg}점)"
    else:
        return f"{student_info.get('name')}님 불합격 (평균: {avg}점)"

output = check_student_pass(student_info)
print(output)

# 문제 12
# [사용자 정의 함수 + 문자열 .replace() + .upper() 융합] 원본 문장(sentence),
# 변경할 단어(old_word), 새 단어(new_word)를 전달받는 함수 sanitize_and_uppercase를 정의하세요.
# 함수 내에서 .replace()로 단어를 치환한 후, 전체 문장을 대문자(.upper())로 변환하여 반환하는 코드를 작성하세요.
def sanitize_and_uppercase(sentence, old_word, new_word):
    output1 = sentence.replace(old_word, new_word)
    output2 = output1.upper()
    return output2

output = sanitize_and_uppercase("python py thon py py thththdas dsafasd", "py", "Java")
print(output)

# 문제 13
# [리스트 + for 반복문 + if 조건문 (최댓값 추적 알고리즘) 융합] 숫자 리스트
# numbers = [15, 42, 88, 23, 71]이 있습니다. max_val 변수에 첫 번째 원소(numbers[0])를 저장한 후, for문과 if
# 조건문만을 사용하여 리스트에서 가장 큰 숫자를 찾아내어 출력하는 코드를 작성하세요.
numbers = [15, 42, 88, 23, 71]
max_val = numbers[0]

for num in numbers:
    if num > max_val:
        max_val = num

print(max_val)

# 문제 14
# [사용자 정의 함수 + 딕셔너리 .values() + for 반복문 융합] 장바구니
# 딕셔너리(cart_dict)를 매개변수로 전달받는 함수 calculate_total_price를 정의하세요.
# 함수 내에서 .values() 함수와 for 반복문을 사용하여 모든 상품 가격을 누적 합산한 총 금액을 반환하고,
# 이를 호출하여 출력하는 코드를 작성하세요.
def calculate_total_price(cart_dict):
    total = 0
    for price in cart_dict.values():
        total += price
    return total

cart = {"1": 5000, "2": 3000, "3": 5500, "4": 8000}
output = calculate_total_price(cart)
print(output)

# 문제 15
# [사용자 정의 함수 + 문자열 .split() + 리스트 인덱싱 + .lower() 융합] 이메일 주소 문자열(email)을
# 매개변수로 받는 함수 extract_domain을 정의하세요. 이메일을 "@" 기호 기준으로
# 분리(.split("@"))한 뒤, 도메인 부분(두 번째 원소)을 소문자(.lower())로 변환하여 반환하고,
# "User_Admin@EXAMPLE.COM"을 대입하여 호출한 결과를 출력하는 코드를 작성하세요.
def extract_domain(email):
    output1 = email.split("@")
    output2 = output1[1].lower()
    return output2

email = "User_Admin@EXAMPLE.COM"
output = extract_domain(email)
print(output)

# 문제 16
# [딕셔너리 .get() + if-else 조건문 + 리스트 .append() 융합] 그룹 데이터
# 딕셔너리 group_data = {"A": ["철수"], "B": ["영희"]}가 있습니다. .get("C")를 이용해 Key "C"가 존재하는지
# 확인한 후, Key가 없으면(None이면) "C" 키에 ["민수"] 리스트를 새로 할당하고, Key가 이미
# 존재하면 해당 리스트에 .append("민수")를 수행하도록 조건을 작성한 뒤 최종 딕셔너리를 출력하세요.
group_data = {"A": ["철수"], "B": ["영희"]}

if group_data.get("C") != None:
    group_data["C"].append("민수")
else:
    group_data["C"] = ["민수"]  # 같은 자료형인 리스트로 작성해야 함

print(group_data)