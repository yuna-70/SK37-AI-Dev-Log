"""TIL: 차원 축소 - PCA 손글씨 데이터 (2026-10-16) — 개념 설명은 README.md 참고"""

# 필요한 라이브러리 / 모듈 / 클래스 / 함수 임포트
import numpy as np
import pandas as pd
import plotly.express as px
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA

# 고차원(64차원) 손글씨 데이터 생성

## 손글씨 데이터 다운로드(data, target 포함)
digits = load_digits()

## feature(X_data) 추출
X_digits = digits.data
print(X_digits)
print(f"데이터의 모양: {X_digits.shape}")

print("-" * 80)

## 정답 컬럼 -> 0~9까지 숫자 추출
y_digits = digits.target
print(y_digits)

print("-" * 80)

## 숫자별 빈도수(정답 항목별 빈도수 -> np.unique(ar, return_counts=True))
output = np.unique(ar=y_digits, return_counts=True)
print(f"정답 항목별 빈도수: \n{output}")

# PCA 모델 생성 및 데이터 변환

## 목표1: 64차원 -> 2차원으로 축소(시각화 목적)

### 주성분 2개인 PCA 변환 모델 생성
pca_2d = PCA(n_components=2, random_state=0)

### fit_transform() 함수 호출, 2차원 변환
X_digits_2d = pca_2d.fit_transform(X_digits)
print(X_digits_2d)
print("-" * 80)
print(f"변환된 데이터의 모양: {X_digits_2d.shape}")

## 목표2: 원본 정보의 95%를 유지하는 차원 축소

### n_components: 0과 1 사이의 실수를 전달하면 해당 비율의 정보를 보존하는 주성분의 수(차원) 자동 계산
pca_95 = PCA(n_components=0.95, random_state=0)

### fit_transform() 함수 호출, 변환
X_digits_95 = pca_95.fit_transform(X_digits)
print(f"변환된 데이터의 모양: {X_digits_95.shape}")

### DataFrame으로 변환 결과 확인
df_95 = pd.DataFrame(data=X_digits_95)
display(df_95)