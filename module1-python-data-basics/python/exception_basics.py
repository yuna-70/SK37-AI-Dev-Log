"""TIL: 예외 처리 - try/except (명시적/포괄적) (2026-09-11) — 개념 설명은 README.md 참고"""

# 명시적 예외 처리(1) - 변수 이름 오타로 NameError 발생시키기
name = "이순신"

try:
    print(f"나라를 구한 위대한 영웅이신 {naem}장군님")  # naem: 오타(존재하지 않는 변수)
except NameError as e:
    print(e)

# 명시적 예외 처리(2) - ZeroDivisionError
for number in range(0, 10):
    try:
        output = 10 / number
        print(output)
    except ZeroDivisionError as e:
        print(e)

# 명시적 예외 처리(3) - 여러 종류의 예외를 각각 처리
# 명시적 예외 처리는 지정한 에러만 처리 가능, 여러 개의 명시적 예외를 동시에 지정할 수 있음
name = "이순신"

try:
    print(f"나라를 구한 위대한 영웅이신 {naem}장군님")
except ZeroDivisionError as e:
    print(e)
except NameError as e:
    print(e)

# 포괄적 예외 처리(1) - Exception으로 모든 오류 한 번에 처리
for number in range(0, 10):
    try:
        output = 10 / number
        print(output)
    except Exception as e:
        print(e)

# 포괄적 예외 처리(2) - 한 블록에 오류가 여러 개 있을 때
name = "이순신"
number = 0

try:
    print(f"나라를 구한 위대한 영웅이신 {naem}장군님")
    # 위에서 이미 예외가 발생하므로 아래 코드는 실행되지 않음
    print(10 / number)
except Exception as e:
    print(e)