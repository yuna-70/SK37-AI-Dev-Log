"""TIL: PyTorch MLP 회귀 - 보스턴 주택 가격 예측 (2026-10-29) — 개념 설명은 README.md 참고"""

# 환경 설정

## 필요한 라이브러리 / 모듈 / 클래스 / 함수 임포트
import numpy as np
import pandas as pd
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

## 연산 디바이스 설정 (GPU 사용 가능 시 cuda, 아니면 cpu)
"""
torch.cuda: pytorch에서 NVIDIA GPU를 활용한 연산 기능을 제공하는 모듈
torch.cuda.is_available(): True -> GPU 사용 가능
"""
if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

print(f"사용 중인 디바이스: {device}")

## colab과 구글 드라이브 연결
from google.colab import drive

drive.mount("/content/drive")

# 데이터 불러오기

## 파일 경로 설정
file_path = "/content/drive/MyDrive/sk/house_price.csv"

## DataFrame 생성
df = pd.read_csv(file_path)
display(df)

# 학습용과 평가용 데이터 생성

## X_data 생성: 정답 레이블 제거
X_data = df.drop(columns=["medv"])
display(X_data)

## y_data 생성: 정답 레이블 인덱싱
y_data = df["medv"]
print(y_data)

## 75:25의 비율로 분할 -> 회귀는 정답이 연속값이라 stratify를 쓸 수 없음
X_train, X_test, y_train, y_test = train_test_split(
    X_data,
    y_data,
    test_size=0.25,
    random_state=0,
)

## 학습용 데이터 확인: 문제와 정답의 인덱스가 같은지
print(f"X_train의 인덱스: {X_train.index}")
print(f"y_train의 인덱스: {y_train.index}")

# 전처리: 표준화

## 표준화 도구 생성
scaler = StandardScaler()

## 학습용과 평가용 데이터 변환: 학습용 기준(평균, 표준편차)
### 변환의 결과: pandas 자료형(DataFrame) -> 넘파이 배열
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print(X_train_scaled)
print(X_test_scaled)

# PyTorch Tensor 변환 및 디바이스로 이동
"""
넘파이 배열 -> PyTorch 학습에 적합한 형태의 자료형(Tensor)으로 변환
.to(device): 해당 Tensor를 연산할 장치(CPU 또는 GPU)로 보냄
"""
X_train_tensor = torch.FloatTensor(X_train_scaled).to(device)
X_test_tensor = torch.FloatTensor(X_test_scaled).to(device)
y_train_tensor = torch.FloatTensor(y_train.values).to(device)

# PyTorch용 표준 데이터셋 생성 -> 미니 배치 생성 준비 단계
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)

# DataLoader 생성
"""
학습용 데이터 379개, batch_size=16
-> 가득 찬 묶음 23개 + 자투리 11개짜리 1개 = 미니 배치 총 24개
-> 검산: (16 * 23) + 11 = 379
"""
train_loader = DataLoader(train_dataset, batch_size=16, shuffle=True)

# MLP 회귀 모델 생성

## 입력 특성(컬럼) 수 추출
input_dim = X_train_tensor.shape[1]
print(f"입력 데이터 특성의 수: {input_dim}")

## nn.Sequential 클래스 사용: 입력층 -> 은닉층1 -> 은닉층2 -> 출력층으로 구성
model = nn.Sequential(
    nn.Linear(input_dim, 64),   # [입력층 -> 은닉층1]: 입력 13개, 인공 뉴런 64개
    nn.ReLU(),                  # [활성화 함수]: 비선형 연산(음수 -> 0)
    nn.Linear(64, 32),          # [은닉층1 -> 은닉층2]: 입력 64개, 인공 뉴런 32개
    nn.ReLU(),                  # [활성화 함수]: 비선형 연산(음수 -> 0)
    nn.Linear(32, 1),           # [은닉층2 -> 출력층]: 출력 뉴런 1개 -> 주택 가격 예측값
).to(device)

print(f"생성된 모델 아키텍처: \n{model}")

# 손실 함수 설정

## 회귀 문제의 손실 함수: 평균 제곱 오차(MSE)
### 출력층에 활성화 함수가 없음 -> 항등 함수 -> 예측값을 그대로 사용
criterion = nn.MSELoss()

# 최적화 알고리즘 설정

## Adam 적용(SGD 개선)
optimizer = optim.Adam(model.parameters(), lr=0.005)

# 모델 학습

## 학습 횟수 설정
epochs = 200

## 모델을 학습 모드로 전환
model.train()

## for 반복문 이용 학습 진행
for epoch in range(epochs):

    ### 손실값 초기화
    epoch_loss = 0.0

    for batch_x, batch_y in train_loader:
        #### 1) 기울기 초기화(이전 학습의 결과물 삭제)
        optimizer.zero_grad()

        #### 2) 순전파 연산 (출력층 뉴런 입력의 총합 -> 예측값)
        predictions = model(batch_x)

        #### 3) 손실 계산 (batch_y를 (batch_size, 1) 모양으로 맞춰줌)
        loss = criterion(predictions, batch_y.unsqueeze(1))

        #### 4) 오차역전파 (가중치별 기울기 산출)
        loss.backward()

        #### 5) 가중치 매개변수 갱신
        optimizer.step()

        #### 손실값 업데이트: PyTorch Tensor 자료형 -> 파이썬 숫자형으로 변환
        epoch_loss += loss.item()

    ### 20 에포크마다 진행 상황 출력
    if (epoch + 1) % 20 == 0:
        avg_loss = epoch_loss / len(train_loader)
        print(f"Epoch [{epoch+1}/{epochs}], Train MSE Loss: {avg_loss:.4f}")

# 모델 평가

## 모델을 평가 모드로 전환
model.eval()

## 평가용 데이터를 이용한 예측: 평가 시에는 기울기 계산 비활성화
with torch.no_grad():
    ### 출력 뉴런의 입력 신호의 총합(예측값) 도출
    ### .cpu(): GPU에 있는 Tensor를 CPU로 가져옴 -> .numpy(): 넘파이 배열로 변환
    test_preds = model(X_test_tensor).cpu().numpy()

## 성능 평가: RMSE 계산
rmse_mlp = root_mean_squared_error(y_test, test_preds)

print(f"[보스턴 주택 가격 예측] PyTorch MLP 평가 RMSE: {rmse_mlp:.4f}")