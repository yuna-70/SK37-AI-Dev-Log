"""TIL: BERT 미세 조정으로 네이버 영화 리뷰 감성 분석 (2026-11-10) — 개념 설명은 README.md 참고"""

import warnings
import numpy as np
import pandas as pd
import torch
from tqdm import tqdm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from transformers import (
    AutoTokenizer,
    BertConfig,
    BertForSequenceClassification,
    Trainer,
    TrainingArguments,
)

warnings.filterwarnings("ignore")


# 1. 학습용 데이터 생성
## 네이버 영화 리뷰(NSMC) 데이터는 탭으로 구분되어 있음
file_path = "ratings_train.txt"
df_train = pd.read_csv(file_path, sep="\t")

print(df_train)

## 누락 데이터 확인 후 제거
num_nulls = df_train.isnull().sum()
print(f"각 컬럼별 누락 데이터의 수: \n{num_nulls}")

df_train1 = df_train.dropna(ignore_index=True)
print(f"누락 제거 후 학습용 데이터: {len(df_train1)}건")

## 정답 레이블의 균형 확인
y_train_counts = df_train1["label"].value_counts(normalize=True)
print(f"정답 레이블의 비율: \n{y_train_counts}")


# 2. 학습용 / 검증용 데이터 분할
X_train_data = df_train1["document"].tolist()
y_train_data = df_train1["label"].tolist()

X_train, X_val, y_train, y_val = train_test_split(
    X_train_data,
    y_train_data,
    test_size=0.2,
    random_state=0,
    stratify=y_train_data,
)


# 3. 평가용 데이터 생성
file_path = "ratings_test.txt"
df_test = pd.read_csv(file_path, sep="\t")

num_nulls = df_test.isnull().sum()
print(f"각 컬럼별 누락 데이터의 수: \n{num_nulls}")

df_test1 = df_test.dropna(ignore_index=True)
print(f"누락 제거 후 평가용 데이터: {len(df_test1)}건")

X_test = df_test1["document"].tolist()
y_test = df_test1["label"].tolist()


# 4. 모델별 토크나이저 생성
## 4-1. 사전 학습된 다국어 BERT 토크나이저
model_name = "google-bert/bert-base-multilingual-cased"
multi_tokenizer = AutoTokenizer.from_pretrained(model_name)

## 4-2. 사전 학습된 한국어 BERT 토크나이저
model_name = "klue/bert-base"
klue_tokenizer = AutoTokenizer.from_pretrained(model_name)

## 4-3. 같은 문장으로 토큰화 결과 비교
def inspect_tokenization(tokenizer, name):
    text = "너와 함께한 시간 모두 눈부셨다. 날이 좋아서 날이 좋지 않아서 날이 적당해서 모든 날이 좋았다."
    result = tokenizer.tokenize(text)
    print(f"[{name}] 토큰화 결과: \n{result}")
    print(f"[{name}] 토큰 수: {len(result)}개")
    print("-" * 80)


inspect_tokenization(multi_tokenizer, "Multilingual BERT")
inspect_tokenization(klue_tokenizer, "KLUE BERT")


# 5. max_length 결정: 리뷰별 토큰 수의 분위수로 근거 만들기
data = df_train1["document"]

## 5-1. 다국어 토크나이저 기준 토큰 수
total_length_multi = []
for review in tqdm(data):
    review_length = len(multi_tokenizer.tokenize(review))
    total_length_multi.append(review_length)

## 5-2. 한국어 토크나이저 기준 토큰 수
total_length_klue = []
for review in tqdm(data):
    review_length = len(klue_tokenizer.tokenize(review))
    total_length_klue.append(review_length)

## 5-3. 90분위수 추출 -> 토크나이저마다 다른 값이 나옴
number_multi = np.percentile(a=total_length_multi, q=90)
number_klue = np.percentile(a=total_length_klue, q=90)

print(f"다국어 토크나이저 90분위수: {number_multi}")
print(f"한국어 토크나이저 90분위수: {number_klue}")


# 6. 모델 입력 데이터 생성
## 토크나이저가 input_ids, attention_mask, token_type_ids 세 가지를 만들어줌
## max_length는 5번에서 구한 분위수를 토크나이저별로 다르게 적용
multi_train_input = multi_tokenizer(X_train, truncation=True, padding=True, max_length=50, return_tensors="pt")
multi_val_input = multi_tokenizer(X_val, truncation=True, padding=True, max_length=50, return_tensors="pt")
multi_test_input = multi_tokenizer(X_test, truncation=True, padding=True, max_length=50, return_tensors="pt")

klue_train_input = klue_tokenizer(X_train, truncation=True, padding=True, max_length=42, return_tensors="pt")
klue_val_input = klue_tokenizer(X_val, truncation=True, padding=True, max_length=42, return_tensors="pt")
klue_test_input = klue_tokenizer(X_test, truncation=True, padding=True, max_length=42, return_tensors="pt")


# 7. Custom Dataset 클래스 정의
## Trainer가 딕셔너리 형태로 데이터를 받기 때문에 직접 만들어야 함
class ClassificationDataset(torch.utils.data.Dataset):
    ### 입력 데이터와 정답 레이블을 받아 저장
    def __init__(self, inputs, labels):
        self.inputs = inputs
        self.labels = labels

    ### 분류 모델 입력 형식에 맞춘 딕셔너리를 반환
    def __getitem__(self, idx):
        item = {key: val[idx].clone().detach() for key, val in self.inputs.items()}
        item["labels"] = torch.tensor(self.labels[idx], dtype=torch.long)
        return item

    ### 전체 데이터의 개수를 반환
    def __len__(self):
        return len(self.inputs["input_ids"])


multi_train_dataset = ClassificationDataset(multi_train_input, y_train)
multi_val_dataset = ClassificationDataset(multi_val_input, y_val)
multi_test_dataset = ClassificationDataset(multi_test_input, y_test)

klue_train_dataset = ClassificationDataset(klue_train_input, y_train)
klue_val_dataset = ClassificationDataset(klue_val_input, y_val)
klue_test_dataset = ClassificationDataset(klue_test_input, y_test)


# 8. 평가 함수 정의
## Trainer가 학습 중간에 호출하는 함수
def compute_metrics(pred):
    labels = pred.label_ids
    ### 출력 뉴런 2개 중 값이 큰 쪽의 인덱스를 예측값으로
    preds = pred.predictions.argmax(-1)
    accuracy = accuracy_score(labels, preds)
    return {"accuracy": accuracy}


# 9. 다국어 BERT 미세 조정
## 9-1. 사전 학습된 모델 불러오기
## num_labels=2 -> 출력층 뉴런 2개(긍정, 부정)로 새로 붙임
model_name = "google-bert/bert-base-multilingual-cased"
num_labels = 2
config = BertConfig.from_pretrained(model_name, num_labels=num_labels)
multi_model = BertForSequenceClassification.from_pretrained(model_name, config=config)

## 9-2. 학습 환경 설정
multi_training_args = TrainingArguments(
    ### 출력 설정
    output_dir="./multi",
    ### 학습 규모 및 배치 크기 설정
    num_train_epochs=1,
    per_device_train_batch_size=128,
    per_device_eval_batch_size=64,
    ### 최적화 설정
    learning_rate=0.0001,
    weight_decay=0.01,
    ### 검증 및 저장 설정
    eval_strategy="epoch",
    save_strategy="epoch",
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    load_best_model_at_end=True,
    save_total_limit=1,
    ### 시각화 도구 사용 설정
    report_to="none",
)

## 9-3. Trainer 생성 및 학습
multi_trainer = Trainer(
    model=multi_model,
    args=multi_training_args,
    train_dataset=multi_train_dataset,
    eval_dataset=multi_val_dataset,
    processing_class=multi_tokenizer,
    compute_metrics=compute_metrics,
)

multi_trainer.train()

## 9-4. 평가
multi_performance = multi_trainer.evaluate(multi_test_dataset)
print(f"Multilingual BERT 평가용 데이터 성능: {multi_performance}")


# 10. 한국어 BERT 미세 조정
## 10-1. 사전 학습된 모델 불러오기
model_name = "klue/bert-base"
config = BertConfig.from_pretrained(model_name, num_labels=num_labels)
klue_model = BertForSequenceClassification.from_pretrained(model_name, config=config)

## 10-2. 학습 환경 설정 (다국어 모델과 동일 조건으로 공정 비교)
klue_training_args = TrainingArguments(
    output_dir="./klue",
    num_train_epochs=1,
    per_device_train_batch_size=128,
    per_device_eval_batch_size=64,
    learning_rate=0.0001,
    weight_decay=0.01,
    eval_strategy="epoch",
    save_strategy="epoch",
    metric_for_best_model="eval_loss",
    greater_is_better=False,
    load_best_model_at_end=True,
    save_total_limit=1,
    report_to="none",
)

## 10-3. Trainer 생성 및 학습
klue_trainer = Trainer(
    model=klue_model,
    args=klue_training_args,
    train_dataset=klue_train_dataset,
    eval_dataset=klue_val_dataset,
    processing_class=klue_tokenizer,
    compute_metrics=compute_metrics,
)

klue_trainer.train()

## 10-4. 평가
klue_performance = klue_trainer.evaluate(klue_test_dataset)
print(f"KLUE BERT 평가용 데이터 성능: {klue_performance}")


# 11. 미세 조정한 모델 저장하고 다시 불러오기
## 11-1. 저장
save_path = "./kor_finetuned_model"
klue_trainer.save_model(save_path)

## 11-2. 불러오기
loaded_klue_model = BertForSequenceClassification.from_pretrained(save_path)
print(f"미세 조정된 모델의 정답 레이블: {loaded_klue_model.config.id2label}")

## 11-3. 불러온 모델로 평가 -> 저장 전과 같은 성능이 나와야 정상
loaded_klue_trainer = Trainer(
    model=loaded_klue_model,
    compute_metrics=compute_metrics,
)

loaded_performance = loaded_klue_trainer.evaluate(klue_test_dataset)
print(f"불러온 모델의 평가용 데이터 성능: {loaded_performance}")