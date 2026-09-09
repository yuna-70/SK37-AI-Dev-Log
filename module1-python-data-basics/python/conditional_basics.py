"""TIL: 조건문 if/elif/else 기본 (2026-09-09) — 개념 설명은 README.md 참고"""

# if 조건문
money = 9900
output = (money >= 10000)
print(f"비교 연산의 결과: {output}")

print("-" * 80)

if money >= 10000:
    print("택시를 탄다")

# if-else 조건문
money = 9900

if money >= 10000:
    print("택시를 탄다")
else:
    print("걸어간다")

# if-elif-else 조건문
money = 1200

if money >= 15000:
    print("택시를 탄다")
elif money >= 4000:
    print("광역 버스를 탄다")
elif money >= 2000:
    print("지하철을 탄다")
else:
    print("걸어간다")

# if-elif-else 실습: 학점 계산기
score = 83

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"나의 등급: {grade}")