"""TIL: HuggingFace pipeline으로 감성 분석 추론 (2026-11-10) — 개념 설명은 README.md 참고"""

import pandas as pd
from transformers import pipeline


# 1. 기본 모델로 감성 분석
## model을 지정하지 않으면 영어 전용 기본 모델이 자동 선택됨
## distilbert-base-uncased-finetuned-sst-2-english
classifier = pipeline(task="text-classification")

text = ["The restaurant is awesome", "The restaurant is awful"]
preds = classifier(text)

print(f"감성 분석의 결과: \n{preds}")


# 2. 영어 경제 기사 전용 모델
## 도메인에 맞게 학습된 모델을 model 매개변수로 지정
model_name = "ProsusAI/finbert"
fin_classifier = pipeline(task="text-classification", model=model_name)

text = ["Stocks rallied and the British pound gained."]
pred = fin_classifier(text)

print(f"finbert 모델로 감성 분석을 한 결과: \n{pred}")


# 3. 한국어 경제 기사 전용 모델
model_name = "snunlp/KR-FinBert-SC"
kor_fin_classifier = pipeline(task="text-classification", model=model_name)

text = [
    "반도체 주도 강세에…코스피 사상 첫 6,600선 넘었다",
    "지난달 120만원대를 웃돌던 삼천당제약 주가가 22일 장중 30만원대까지 떨어졌다.",
]
preds = kor_fin_classifier(text)

print(f"첫 번째 경제 기사 감성 분석의 결과: \n{preds[0]}")
print("-" * 80)
print(f"두 번째 경제 기사 감성 분석의 결과: \n{preds[1]}")


# 4. 한국어 영화 리뷰 전용 모델
## 이 모델은 결과 레이블이 LABEL_0 / LABEL_1로 나옴
model_name = "doya/klue-sentiment-nsmc"
kor_classifier = pipeline(task="text-classification", model=model_name)

text = [
    "음악이 주가 된, 최고의 음악영화",
    "절대 봐서는 안 될 영화.. 재미도 없고 기분만 잡치고.. 한 세트장에서 다 해먹네",
]
preds = kor_classifier(text)

print(f"첫 번째 영화 리뷰 감성 분석 결과: \n{preds[0]}")
print("-" * 80)
print(f"두 번째 영화 리뷰 감성 분석 결과: \n{preds[1]}")


# 5. 마켓컬리 리뷰 데이터 감성 분석
## 5-1. 데이터 불러오기
file_path = "kurly_reviews.csv"
df = pd.read_csv(file_path)

print(df)

## 리뷰 컬럼만 리스트로 변환
all_reviews = df["리뷰"].tolist()

print(f"리뷰 데이터의 개수: {len(all_reviews)}개")

## 5-2. 첫 번째 모델로 감성 분석
### truncation=True: 모델 최대 길이를 넘는 텍스트는 자동으로 자름
sentiment_output1 = kor_classifier(all_reviews, truncation=True)

### LABEL_0 / LABEL_1을 읽을 수 있는 값으로 변환
label_list = []
for output in sentiment_output1:
    label = output.get("label")
    if label == "LABEL_1":
        label = "positive"
    else:
        label = "negative"
    label_list.append(label)

df["label"] = label_list

## 5-3. 두 번째 모델로 감성 분석
### task 없이 model만 지정해도 모델 설정에서 작업 종류를 알아냄
kor_classifier1 = pipeline(model="whitepeak/bert-base-cased-korean-sentiment")

sentiment_output2 = kor_classifier1(all_reviews, truncation=True)

label_list = []
for output in sentiment_output2:
    label = output.get("label")
    if label == "LABEL_1":
        label = "positive"
    else:
        label = "negative"
    label_list.append(label)

df["label1"] = label_list

print(df)


# 6. 두 모델의 결과 비교
## 6-1. 긍정 부정 빈도수 측정
sentiment_count1 = df["label"].value_counts()
sentiment_count2 = df["label1"].value_counts()

print(f"첫 번째 감성 분석 모델의 긍정 부정의 빈도수: \n{sentiment_count1}")
print("-" * 80)
print(f"두 번째 감성 분석 모델의 긍정 부정의 빈도수: \n{sentiment_count2}")

## 6-2. 부정으로 판정된 리뷰 확인
df_neg_reviews1 = df.query("label=='negative'")
df_neg_reviews2 = df.query("label1=='negative'")

print("첫 번째 감성 분석 모델의 부정 리뷰")
print(df_neg_reviews1)
print("-" * 80)
print("두 번째 감성 분석 모델의 부정 리뷰")
print(df_neg_reviews2)