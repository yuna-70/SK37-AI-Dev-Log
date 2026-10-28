"""TIL: PyTorch MLP 이진 분류 - 타이타닉 생존 예측 (2026-10-28) — 개념 설명은 README.md 참고"""

# 환경 설정

## 필요한 라이브러리 / 모듈 / 클래스 / 함수 임포트
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader

## 연산 장치(디바이스) 설정
"""
torch.cuda: pytorch에서 NVIDIA GPU를 활용한 연산과 GPU 메모리를 관리하는 모듈
torch.cuda.is_available(): NVIDIA 그래픽 카드를 사용할 수 있는지 확인 -> True면 GPU 사용 가능
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
file_path = "/content/drive/MyDrive/sk/titanic_cleaned.csv"

## DataFrame 생성
df = pd.read_csv(file_path)
display(df)

# 학습용과 평가용 데이터 생성

## X_data 생성: 정답 컬럼 제거
X_data = df.drop(columns=["Survived"])

## y_data 생성: 정답 컬럼 인덱싱
y_data = df["Survived"]

## 80:20의 비율로 분할 -> 무작위성 통제 -> random_state, stratify
X_train, X_test, y_train, y_test = train_test_split(
    X_data,
    y_data,
    test_size=0.2,
    random_state=0,
    stratify=y_data
)

## 학습용 데이터 확인: 인덱스와 정답 비율
print(f"X_train의 인덱스: {X_train.index}")
print(f"y_train의 인덱스: {y_train.index}")

ratio = y_train.value_counts(normalize=True)
print(f"학습용 데이터의 정답별 비율: \n{ratio}")

# 전처리: 표준화

## 표준화 도구 생성
scaler = StandardScaler()

## 학습용과 평가용 데이터 변환: 학습용 기준(평균, 표준편차)
### 변환의 결과: pandas 자료형(DataFrame, Series) -> 넘파이 배열
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# PyTorch Tensor 변환
"""
자동 미분, 역전파, GPU 상의 연산 기능을 추가하기 위해 넘파이 배열을 Tensor로 변환
torch.FloatTensor(넘파이배열): 실수형 자료형
torch.LongTensor(넘파이배열): 정수형 자료형
"""
X_train_tensor = torch.FloatTensor(X_train_scaled)
X_test_tensor = torch.FloatTensor(X_test_scaled)
y_train_tensor = torch.FloatTensor(y_train.values)
y_test_tensor = torch.FloatTensor(y_test.values)

print(X_train_tensor)
print(y_train_tensor)

# PyTorch용 표준 데이터셋 생성
"""
1. 학습용 문제(X_train_tensor)와 정답(y_train_tensor)을 하나의 쌍으로 묶어준다.
2. 이유: 학습용 데이터를 미니 배치(N) 단위로 샘플링해야 하므로, 서로의 인덱스를
   동일하게 만들기 위해 문제와 정답을 하나의 쌍으로 묶어서 관리 -> TensorDataset 클래스
"""
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)

# DataLoader 생성
"""
1. 딥러닝의 학습: 미니 배치 단위
2. 데이터를 미니 배치 단위로 샘플링해서 모델에게 공급해주는 도구
3. 미니 배치의 개수 계산
   - 학습용 데이터 1,046개, 미니 배치의 크기 32개
   - 가득 찬 묶음 32개 + 자투리 22개짜리 1개 = 총 33개
   - 검산: (32 * 32) + 22 = 1046
"""
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

# MLP 분류 모델 생성

## 입력 특성 수 추출
input_dim = X_train_tensor.shape[1]
print(f"입력 데이터의 특성의 수: {input_dim}")

## nn.Sequential 클래스 사용: 입력층 -> 은닉층1 -> 은닉층2 -> 출력층으로 구성
binary_model = nn.Sequential(
    nn.Linear(input_dim, 32),   # [입력층 -> 은닉층1]: 입력 10개, 인공 뉴런 32개
    nn.ReLU(),                  # [활성화 함수]: 비선형 연산(음수 -> 0)
    nn.Linear(32, 16),          # [은닉층1 -> 은닉층2]: 입력 32개, 인공 뉴런 16개
    nn.ReLU(),                  # [활성화 함수]: 비선형 연산(음수 -> 0)
    nn.Linear(16, 1),           # [은닉층2 -> 출력층]: 입력 16개, 출력 뉴런 1개
)

print(f"생성된 모델 아키텍처: \n{binary_model}")

# 손실 함수 설정

## 시그모이드와 이진 교차 엔트로피(BCE)를 결합한 BCEWithLogitsLoss 클래스 적용
### 모델의 마지막에 시그모이드를 넣지 않는 이유: 손실 함수가 내부에서 처리함
criterion = nn.BCEWithLogitsLoss()

# 최적화 알고리즘 설정
"""
parameter vs hyperparameter
1) parameter: 사람이 설정하지 않고 모델의 학습을 통해서만 변하는 매개 변수 -> W, b
2) hyperparameter: 사람이 설정 -> 뉴런의 수, max_depth, min_samples_leaf, learning_rate
"""

"""
학습 횟수 = Epoch
1. 딥러닝 학습: 전체 데이터를 미니 배치(N) 단위로 샘플링
2. 미니 배치 1개 단위의 학습 = Step
3. 미니 배치 묶음 전체를 학습하면 전체 데이터를 1회 학습 완료 = 1 Epoch
4. Epoch마다 미니 배치를 새롭게 샘플링하므로, Epoch=1일 때와 Epoch=2일 때의
   미니 배치 데이터 구성이 다르다.
"""

## Adam 적용(SGD 개선)
"""
1. 학습의 대상 -> parameter -> 뉴런의 가중치와 편향(W, b)
2. Adam() 클래스 첫 번째 매개변수 -> params = model.parameters()
3. Adam() 클래스 두 번째 매개변수 -> lr(학습률) = 0.001(기본값)
"""
optimizer = optim.Adam(params=binary_model.parameters(), lr=0.005)

# 모델 학습

## 학습 횟수 설정
epochs = 50

## 모델을 훈련 모드로 설정
binary_model.train()

## for 반복문 이용 학습 진행
for epoch in range(epochs):

    ### 손실값 초기화
    epoch_loss = 0.0

    for batch_x, batch_y in train_loader:
        #### 1) 기울기 초기화(이전 학습의 결과물 삭제)
        optimizer.zero_grad()

        #### 2) 순전파 연산 (출력층 뉴런 입력의 총합)
        outputs = binary_model(batch_x)

        #### 3) 손실 계산 (batch_y를 (N, 1) 모양으로 맞춰줌)
        loss = criterion(outputs, batch_y.unsqueeze(1))

        #### 4) 오차역전파 (가중치별 기울기 산출)
        loss.backward()

        #### 5) 가중치 매개변수 갱신
        optimizer.step()

        #### 손실값 업데이트: PyTorch Tensor 자료형 -> 파이썬 숫자형으로 변환
        epoch_loss += loss.item()

    ### 10 에포크마다 진행 상황 출력
    if (epoch + 1) % 10 == 0 or epoch == 0:
        avg_loss = epoch_loss / len(train_loader)
        print(f"Epoch [{epoch+1}/{epochs}], Train BCE Loss: {avg_loss:.4f}")
        