"""TIL: 수치 미분과 경사하강법 (2026-10-26) — 개념 설명은 README.md 참고"""

# 필요한 라이브러리 임포트
import numpy as np

# 수치 미분 함수 정의
"""
f: 미분할 대상 파이썬 함수
x: 미분을 수행할 목표 지점
"""
def numerical_diff(f, x):
    h = 0.0001
    output = (f(x + h) - f(x - h)) / (2 * h)
    return output

# 미분을 할 대상 파이썬 함수 정의
def function(x):
    return x**2

# 미분을 수행할 목표 지점 설정
target_x = 3.0

# 해석적 미분(df/dx = 2x)과 수치 미분 비교

## 해석적 미분 시행
output1 = 2 * target_x
print(f"미분 수행 지점(x): {target_x}")
print(f"해석적 미분(이론 참값): {output1}")

## 수치 미분 실행
### 파이썬의 특징 -> 함수가 다른 함수의 입력 값으로 사용 가능
output2 = numerical_diff(function, target_x)
print(f"수치 미분(컴퓨터 계산): {output2:.1f}")