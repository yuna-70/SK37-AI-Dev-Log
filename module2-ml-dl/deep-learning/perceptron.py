"""TIL: 퍼셉트론 구현과 논리 게이트 (2026-10-23) — 개념 설명은 README.md 참고"""

# 필요한 라이브러리 임포트
import numpy as np

# 기초 과정

## 파이썬 리스트 -> 넘파이 배열
arr = np.array([1, 2, 3])
print(arr)

## np.sum(arr) -> 배열의 각 성분 원소의 합
output = np.sum(arr)
print(output)

## 배열 간의 곱 -> 같은 위치의 원소끼리 곱함

### 배열 생성
arr1 = np.array([0, 1])
print(f"배열1: {arr1}")
arr2 = np.array([0.5, 0.5])
print(f"배열2: {arr2}")

### 배열 간의 곱 실행
output = arr1 * arr2
print(f"두 배열 간의 곱셈: {output}")

### 곱셈의 결과 -> "합" 연산 -> 퍼셉트론의 입력 신호의 총합과 같은 형태
output1 = np.sum(output)
print(f"두 배열 간의 곱셈의 결과에 대한 합: {output1}")

# 퍼셉트론 실습

## 가중치와 편향을 활용한 직선식 -> AND 게이트 구현
def AND(x1, x2):
    x = np.array([x1, x2])      # 입력 신호 구현
    w = np.array([0.5, 0.5])    # 퍼셉트론 직선식의 가중치 구현
    b = -0.7                    # 퍼셉트론 직선식의 편향 구현
    output = np.sum(x * w) + b  # 입력 신호의 총합

    # 입력 신호의 총합에 대한 의미 부여(정답 레이블 예측: 0과 1로 분류)
    if output >= 0:
        return 1
    else:
        return 0

## 가중치와 편향을 활용한 퍼셉트론 표현 -> NAND 게이트 구현
def NAND(x1, x2):
    x = np.array([x1, x2])      # 입력 신호 구현
    w = np.array([-0.5, -0.5])  # 퍼셉트론 직선식의 가중치 구현(AND와 정반대)
    b = 0.7                     # 퍼셉트론 직선식의 편향 구현(AND와 정반대)
    output = np.sum(x * w) + b  # 입력 신호의 총합

    if output >= 0:
        return 1
    else:
        return 0

## 가중치와 편향을 활용한 OR 게이트 구현
def OR(x1, x2):
    x = np.array([x1, x2])      # 입력 신호 구현
    w = np.array([0.5, 0.5])    # 퍼셉트론 직선식의 가중치 구현(AND와 동일)
    b = -0.2                    # 퍼셉트론 직선식의 편향 구현(AND보다 크게 설정)
    output = np.sum(x * w) + b  # 입력 신호의 총합

    if output >= 0:
        return 1
    else:
        return 0

## 논리 게이트의 조합을 통한 다층 퍼셉트론(MLP) -> XOR 게이트 구현
def XOR(x1, x2):
    # 은닉층 구현: 입력값을 두 가지 서로 다른 논리 게이트로 나누어서 처리(병렬)
    s1 = NAND(x1, x2)
    s2 = OR(x1, x2)

    # 출력층 구현: 은닉층의 결과를 조합(입력 신호의 변형), 결과 도출
    output = AND(s1, s2)
    return output

# 논리 게이트 진리표 생성

## 입력값 설정
inputs = [(0, 0), (1, 0), (0, 1), (1, 1)]

## AND 게이트
for x in inputs:
    ### 인덱싱 -> 두 개의 입력값 설정
    x1 = x[0]
    x2 = x[1]
    ### AND 연산 실행 및 결과 출력
    output = AND(x1, x2)
    print(f"입력(input): {x} -> 결과(output): {output}")

print("-" * 80)

## NAND 게이트
for x in inputs:
    x1 = x[0]
    x2 = x[1]
    output = NAND(x1, x2)
    print(f"입력: {x} -> 결과: {output}")

print("-" * 80)

## OR 게이트
for x in inputs:
    x1 = x[0]
    x2 = x[1]
    output = OR(x1, x2)
    print(f"입력: {x} -> 결과: {output}")

print("-" * 80)

## XOR 게이트
for x in inputs:
    x1 = x[0]
    x2 = x[1]
    output = XOR(x1, x2)
    print(f"입력: {x} -> 출력: {output}")