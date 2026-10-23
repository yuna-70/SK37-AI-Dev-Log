"""TIL: 활성화 함수 - 계단·시그모이드·ReLU·소프트맥스 (2026-10-23) — 개념 설명은 README.md 참고"""

# 필요한 라이브러리 임포트
import numpy as np
import pandas as pd

# 계단 함수

## np.where(조건식, True일 때 값, False일 때 값)
### 조건이 참인 곳에는 x를, 거짓인 곳에는 y를 채워서 새로운 배열 생성

### 넘파이 배열 생성
arr = np.array([0.3, -1.4, 1.2, -0.2])
print(arr)

### 입력값 -> 0이상이면 1, 0미만이면 0으로 변경
output = np.where(arr >= 0, 1, 0)
print(output)

## 계단 함수 정의: 입력값이 0미만이면 0, 0이상이면 1
def step_function(x):
    output = np.where(x >= 0, 1, 0)
    return output

## 인공 뉴런 정의: 입력 신호 -> 입력 신호의 총합을 구한다
### 활성화 함수와 분리하기 위해 총합까지만 계산하고 반환
def perceptron(x1, x2):
    x = np.array([x1, x2])      # 입력 신호 구현
    w = np.array([0.5, 0.5])    # 퍼셉트론 직선식의 가중치 구현
    b = -0.7                    # 퍼셉트론 직선식의 편향 구현
    output = np.sum(x * w) + b  # 입력 신호의 총합
    return output

## 인공 뉴런(perceptron) + 활성화 함수(step_function) 연결 -> AND 게이트 결과 재현

### 입력 데이터 생성
inputs = [(0, 0), (1, 0), (0, 1), (1, 1)]

### for문 작성
for x in inputs:
    #### 인덱싱 -> 두 개의 입력값 생성
    x1 = x[0]
    x2 = x[1]
    #### perceptron 실행
    output1 = perceptron(x1, x2)
    print(f"perceptron 실행의 결과: {output1}")
    #### 활성화 함수(계단 함수) 실행
    output2 = step_function(output1)
    print(f"계단 함수 실행의 결과: {output2}")
    print("-" * 80)

# 시그모이드 함수

## 0과 1사이의 연속적인 확률값 제공
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

## 인공 뉴런(perceptron) + 활성화 함수(sigmoid 함수)
for x in inputs:
    x1 = x[0]
    x2 = x[1]
    ### perceptron 실행
    output1 = perceptron(x1, x2)
    print(f"출력층 인공 뉴런 실행의 결과: {output1}")
    ### 활성화 함수(sigmoid) 실행
    output2 = sigmoid(output1)
    print(f"sigmoid 함수 실행의 결과(정답이 1일 확률): {output2}")
    print("-" * 80)

# ReLU 함수

## 은닉층 퍼셉트론의 입력 신호의 총합 -> 0이하는 0으로 차단, 양수는 그대로 통과
def relu(x):
    return np.maximum(0, x)

## 은닉층 퍼셉트론 + 활성화 함수(ReLU)

### 은닉층의 퍼셉트론 입력 신호의 총합 -> 가상으로 설정(은닉층 퍼셉트론 7개로 가정)
perceptron_outputs = np.array([-5.0, -2.0, -0.5, 0.0, 0.5, 2.0, 5.0])

### 활성화 함수(ReLU) 실행
output = relu(perceptron_outputs)
print(f"ReLU 함수 실행의 결과: \n{output}")

# 소프트맥스 함수

## 다중 클래스 분류에 사용: 출력 뉴런(정답의 개수)별 입력 신호의 총합 -> 확률 계산
def softmax(arr):
    ### 분자 부분: 각 출력 뉴런의 (입력 신호의 총합) 별로 각각 계산
    exp_arr = np.exp(arr)
    ### 분모 부분: 각 출력 뉴런 별로 계산한 것 -> 총합
    sum_exp_arr = np.sum(exp_arr)
    ### 결과 확인
    output = exp_arr / sum_exp_arr
    return output

## 다중 분류 문제: 정답 3개의 클래스(예: 개, 고양이, 새) 분류

### 출력층 -> 출력 뉴런 3개 -> 각각 입력 신호의 총합 -> 가상으로 설정
output_perceptron_sum = np.array([0.3, 2.9, 4.0])

### 다중 분류 실행: 출력 뉴런 -> 활성화 함수(softmax 함수)
output = softmax(output_perceptron_sum)

### 분류 결과 출력 -> 클래스별 확률
print(f"클래스별 확률: {output}")
print(f"확률의 총합: {np.sum(output)}")