"""TIL: 손실 함수 - MSE·교차 엔트로피 오차 (2026-10-26) — 개념 설명은 README.md 참고"""

# 필요한 라이브러리 임포트
import numpy as np

# 회귀 문제의 손실 함수

## 평균 제곱 오차(MSE): (정답 - 예측)의 제곱에 대한 평균
### t: 실제 정답, y: 모델의 예측값
def mean_squared_error(t, y):
    return np.mean((t - y)**2)

## 정답 생성
target_reg = 2.5

## 정답에 가까운 우수한 예측 생성
y_pred1 = 2.3

## 정답에서 크게 벗어난 저조한 예측 생성
y_pred2 = 0.5

## 오차 연산

### 우수한 예측값의 손실값(MSE)
mse1 = mean_squared_error(target_reg, y_pred1)
print(f"우수한 예측값 ({y_pred1})의 손실 MSE: {mse1:.4f}")

### 저조한 예측값의 손실값(MSE)
mse2 = mean_squared_error(target_reg, y_pred2)
print(f"저조한 예측값 ({y_pred2})의 손실 MSE: {mse2:.4f}")

# 분류 문제의 손실 함수

## 다중 분류 문제의 손실 함수

### 교차 엔트로피 오차(CEE)
"""
t: 원-핫 인코딩 된 정답 레이블 배열
y: 모델의 예측 확률 배열 -> 출력층 softmax의 출력값
"""
def cross_entropy_error(t, y):
    output = -np.sum(t * np.log(y))
    return output

### 예시: 3중 분류 문제

#### 정답 레이블 생성 -> 입력 데이터 -> 세번째 물체
target_multi = np.array([0, 0, 1])

#### 모델 1의 예측: 세번째 물체가 정답이 될 확률을 60%로 가장 높게 예측 (정답 적중)
y_multi1 = np.array([0.1, 0.3, 0.6])

#### 모델 2의 예측: 세번째 물체가 정답이 될 확률을 5%로 매우 낮게 예측 (오답 판정)
y_multi2 = np.array([0.8, 0.15, 0.05])

### 오차 연산

#### 모델 1의 예측에 대한 교차 엔트로피 오차(CEE): 결과 = -log(0.6)
output1 = cross_entropy_error(target_multi, y_multi1)
print(f"정답을 맞힌 모델 1의 CEE: {output1:.4f}")

#### 모델 2의 예측에 대한 교차 엔트로피 오차(CEE): 결과 = -log(0.05)
output2 = cross_entropy_error(target_multi, y_multi2)
print(f"정답을 틀린 모델 2의 CEE: {output2:.4f}")

## 이진 분류 문제의 손실 함수

### 이진 교차 엔트로피 오차(BCE)
"""
t: 실제 정답 레이블(0 또는 1)
y: 모델의 예측 확률 -> 출력 뉴런 1개의 입력 총합 -> sigmoid(0~1 사이의 확률)
"""
def binary_cross_entropy_error(t, y):
    output = -(t * np.log(y) + (1 - t) * np.log(1 - y))
    return output

### 예시: 스팸 메일 판별(정답 t=1: 스팸 메일)

#### 정답
target_binary = 1

#### 모델 1의 예측 -> 스팸일 확률을 80%(0.8)로 예측 (우수한 예측)
y1 = 0.8

#### 모델 2의 예측 -> 스팸일 확률을 20%(0.2)로 예측 (저조한 예측)
y2 = 0.2

### 오차 연산

#### 모델 1의 예측에 대한 BCE 측정: -log(0.8)
loss1 = binary_cross_entropy_error(target_binary, y1)
print(f"정답에 근접한 예측 ({y1})의 BCE: {loss1:.4f}")

#### 모델 2의 예측에 대한 BCE 측정: -log(0.2)
loss2 = binary_cross_entropy_error(target_binary, y2)
print(f"정답에서 벗어난 예측 ({y2})의 BCE: {loss2:.4f}")