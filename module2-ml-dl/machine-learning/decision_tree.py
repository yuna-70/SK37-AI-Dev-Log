"""TIL: 결정 트리 분류 모델 - 붓꽃 품종 분류 (2026-10-12) — 개념 설명은 README.md 참고"""

# 경고 메시지 무시 설정
import warnings
warnings.filterwarnings("ignore")

# 필요한 라이브러리 임포트
import pandas as pd

# 데이터 불러오기
file_path = "iris_dataset.csv"
df_iris = pd.read_csv(file_path)
display(df_iris)

# 데이터 전처리: Label Encoding

## 붓꽃 품종의 label 컬럼의 값 -> 숫자로 변환
## replace()만 쓰면 dtype이 object로 남으므로 astype(int)까지 적용
df_label = df_iris.replace({"setosa": 0, "versicolor": 1, "virginica": 2})
df_label["label"] = df_label["label"].astype(int)
display(df_label)
print(f"label 컬럼의 자료형: {df_label['label'].dtype}")

# 학습용 데이터와 평가용 데이터 생성

## X_data 생성 -> 정답 컬럼을 제외한 나머지 컬럼들
X_data = df_label.drop(columns=["label"])
display(X_data)

## y_data 생성 -> 정답 컬럼만 인덱싱
y_data = df_label["label"]
print(f"정답 데이터(label): \n{y_data}")

## 80:20의 비율로 학습용 데이터와 평가용 데이터 생성
from sklearn.model_selection import train_test_split

### train_test_split() 함수 사용 -> random_state, stratify 적용
X_train, X_test, y_train, y_test = train_test_split(
    X_data,
    y_data,
    test_size=0.2,
    random_state=0,
    stratify=y_data
)

## 학습용 데이터 확인 -> 행 인덱스 확인
print(f"X_train의 행 인덱스: \n{X_train.index}")
print(f"y_train의 행 인덱스: \n{y_train.index}")

## 정답의 품종별 빈도수 확인 -> stratify 적용 결과 확인
y_train_counts = y_train.value_counts()
print(f"학습용 데이터의 정답별 빈도수: \n{y_train_counts}")

# DecisionTree 모델
## 트리 기반 모델은 값의 순서만 보므로 표준화가 필요 없음

## 모델 생성
from sklearn.tree import DecisionTreeClassifier

dt = DecisionTreeClassifier(random_state=0)

## 모델 학습 -> 불순도가 낮아지는 방향으로 데이터를 반복 분할
dt.fit(X_train, y_train)
print("학습 완료")

## 생성된 트리의 구조 확인
print(f"트리의 깊이(depth): {dt.get_depth()}")
print(f"리프 노드의 수: {dt.get_n_leaves()}")

# 모델 학습 시 생성된 의사 결정 트리 시각화

## 필요한 함수 임포트
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

## 이미지 크기 재설정: 기본값(가로 6.4inch, 세로 4.8inch)
plt.figure(figsize=(10, 6))

## plot_tree 함수 호출, 시각화
plot_tree(
    decision_tree=dt,
    feature_names=X_train.columns,
    class_names=["setosa", "versicolor", "virginica"],
    filled=True
)
plt.show()

# 평가용 데이터에 대한 예측
pred_test = dt.predict(X_test)
print(f"평가용 데이터에 대한 예측값: \n{pred_test}")

# 모델 평가

## 필요한 함수 임포트
from sklearn.metrics import accuracy_score

## 평가용 데이터에 대한 성능 평가
accuracy_dt = accuracy_score(y_test, pred_test)
print(f"평가용 데이터에 대한 성능(accuracy): {accuracy_dt}")