"""TIL: 예외 처리 심화 - 명시적/다중/포괄적 예외 처리 (2026-09-11) — 개념 설명은 README.md 참고"""

# 문제 1
# [파일 쓰기("w") + for 반복문 + range() + f-string 융합] with-open 구문과 쓰기 모드("w")를 사용하여 
# "daily_log.txt" 파일을 생성하세요. for 반복문과 range(1, 6)을 활용하여 파일에
# "2026-07-28 작업 기록 1\n"부터 "2026-07-28 작업 기록 5\n"까지 총 5줄의 문자열을
# 기록(f.write())하는 코드를 작성하세요.
file_path = "daily_log.txt"

with open(file=file_path, mode="w", encoding="utf-8") as f:
    for number in range(1, 6):
        data = f"2026-07-28 작업 기록 {number}\n"
        f.write(data)

# 문제 2
# [사용자 정의 함수 + 파일 읽기("r") + try-except FileNotFoundError 융합] 파일 경로
# file_path를 매개변수로 받는 함수 read_file_safely를 정의하세요. with open(..., mode="r")과
# .read() 함수를 사용해 파일 전체 내용을 읽어 반환하되, 존재하지 않는 파일명 입력으로
# FileNotFoundError가 발생할 경우 프로그램이 중단되지 않고 "파일을 찾을 수 없습니다."라는
# 안내 문자열을 반환하도록 명시적 예외 처리를 적용하는 코드를 작성하세요.
file_path = "daily_log.txt"

def read_file_safely(file_path):
    try:
        with open(file=file_path, mode="r") as f:
            return f.read()
    except FileNotFoundError:
        return "파일을 찾을 수 없습니다."

data = read_file_safely(file_path)
print(data)

# 문제 3
# [사용자 정의 함수 + 리스트 인덱싱 + 다중 명시적 예외 처리 융합] 리스트 자료형
# 데이터 data_list와 접근할 인덱스 index를 매개변수로 받는 함수 parse_and_divide를 작성하세요.
# 함수 내부에서 100 // int(data_list[index]) 연산을 수행하여 정수 몫을 반환합니다.
# 단, 다음 3가지 예외 상황에 대해 각각 지정된 메시지를 반환하도록 try-except 블록을 구성하세요.
# - IndexError: "인덱스 범위 초과"
# - ValueError: "숫자 변환 불가"
# - ZeroDivisionError: "0으로 나눌 수 없음"
def parse_and_divide(data_list, index):
    try:
        return 100 // int(data_list[index])
    except IndexError:
        return "인덱스 범위 초과"
    except ValueError:
        return "숫자 변환 불가"
    except ZeroDivisionError:
        return "0으로 나눌 수 없음"

data_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "a"]
index = 0
result = parse_and_divide(data_list, index)
print(result)

# 문제 4
# [파일 읽기(f.readlines()) + 문자열 .strip(), .split() + 딕셔너리 수집 + 포괄적 예외
# 처리(Exception as e) 융합] 파일 경로 file_path를 입력받아 성적 정보를 딕셔너리로 변환하는
# 함수 parse_scores_file을 작성하세요.
# 1. with open(..., mode="r")과 f.readlines()를 활용해 파일의 각 줄을 리스트로 읽어옵니다.
# 2. for문으로 각 줄을 순회하며 .strip()으로 공백/줄바꿈을 제거하고, 쉼표(,)를 기준으로
# .split(",")하여 이름과 점수(정수형 int 변환)를 딕셔너리 score_dict에 Key-Value로 저장합니다.
# 3. 파일 읽기 및 처리 과정 전체를 try-except Exception as e: 블록으로 감싸 예외 발생 시
# "프로그램 실행 중 예측하지 못한 오류가 발생했습니다." 및 오류 유형을 출력하고(print(e)), None을 반환하도록 작성하세요.
def parse_scores_file(file_path):
    file_list = {}
    try:
        with open(file=file_path, mode="r", encoding="utf-8") as f:
            for line in f.readlines():
                line_strip = line.strip()
                if line_strip:
                    name, score = line_strip.split(",")
                    file_list[name] = int(score)
        return file_list
    except Exception as e:
        print("프로그램 실행 중 예측하지 못한 오류가 발생했습니다.")
        print(e)
        return None

with open("scores.txt", mode="w", encoding="utf8") as f:
    f.write("김철수,90\n이영희,85\n박민수,95\n")

data = parse_scores_file("scores.txt")
print(data)