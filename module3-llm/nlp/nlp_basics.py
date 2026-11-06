"""TIL: 자연어 처리 기초 - 토큰화·임베딩·RNN (2026-11-03 ~ 11-06) — 개념 설명은 README.md 참고"""

# 1. 영어 토큰화와 불용어 제거

## 필요한 라이브러리 임포트
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

## 추가 기능 다운로드
nltk.download("punkt_tab")   # 문장을 구분하기 위한 구두점
nltk.download("stopwords")   # 불용어

## 영어 불용어 리스트 생성
stopwords_list = nltk.corpus.stopwords.words("english")
print(f"영어 불용어의 수: {len(stopwords_list)}개")

## 문장 단위 토큰화: 구두점(. ! ?) 기준
output1 = sent_tokenize(text_en)

## 띄어쓰기 기준 토큰화: 영어는 단어, 한글은 어절
output2 = word_tokenize(text_en)

## 불용어 제거
cleaned_words = []
for word in output2:
    ### 소문자로 바꾼 뒤 불용어 리스트와 비교
    if word.lower() not in stopwords_list:
        cleaned_words.append(word)

print(f"불용어 제거 전: {len(output2)}개")
print(f"불용어 제거 후: {len(cleaned_words)}개")

# 2. 서브워드 토큰화: WordPiece

## 단어 사전 학습용 도구
from tokenizers import BertWordPieceTokenizer

tokenizer = BertWordPieceTokenizer(lowercase=False, strip_accents=False)
"""
lowercase: 모두 소문자로 변환할지 여부
strip_accents: 악센트 기호를 떼어낼지 여부
"""

## 말뭉치로 학습 -> 단어 사전 생성
tokenizer.train(files=[file_path1, file_path2], vocab_size=30000)

## 사전을 파일(vocab.txt)로 저장
tokenizer.save_model(save_dir)

## 저장된 사전을 불러와 실제 토큰화에 사용
from transformers import BertTokenizerFast

tokenizer = BertTokenizerFast.from_pretrained(
    save_dir, lowercase=False, strip_accents=False
)

## 토큰화 -> 정수 인코딩
tokens = tokenizer.tokenize(sample_sentence)
token_ids = tokenizer.convert_tokens_to_ids(tokens)

# 3. 한글 형태소 분석

## 형태소 분석 도구 생성
from konlpy.tag import Okt
from mecab import MeCab

okt = Okt()
mecab = MeCab()

## 세 함수는 Okt와 MeCab이 동일
okt.morphs(text)   # 형태소만 추출
okt.pos(text)      # 형태소 + 품사 태깅
okt.nouns(text)    # 명사만 추출

# 4. 빈도수 분석과 시각화

## 텍스트 파일 읽기
with open(file=file_path, mode="r") as f:
    text = f.read()

## 명사 추출 후 길이가 1보다 큰 것만 남기기
nouns_okt = okt.nouns(text)

final_nouns_okt = []
for noun in nouns_okt:
    if len(noun) > 1:
        final_nouns_okt.append(noun)

## 빈도수 분석
from collections import Counter

counts_okt = Counter(final_nouns_okt)

## WordCloud 시각화
from wordcloud.wordcloud import WordCloud

font = "/usr/share/fonts/truetype/nanum/NanumBarunGothic-YetHangul.ttf"

wordcloud = WordCloud(
    font_path=font,          # 한글 폰트 경로, 없으면 글자가 깨짐
    width=1000,
    height=500,
    max_words=50,            # 빈도수 상위 50개만
    background_color="white",
    colormap="tab10",
    random_state=0,
)

## 이미 세어둔 빈도수를 넣음 (원본 텍스트를 넣는 generate()와 다름)
wordcloud.generate_from_frequencies(counts_okt)
wordcloud.to_file(save_path)

# 5. 임베딩: CountVectorizer

## 임베딩 도구 생성
from sklearn.feature_extraction.text import CountVectorizer

ko_cv = CountVectorizer()

## 말뭉치 생성
ko_text = [
    "나는 배가 고프다",
    "내일 점심 뭐먹지",
    "내일 공부 해야겠다",
    "점심 먹고 공부해야지",
]

## fit(): 어절 단위로 토큰화 -> 단어 사전 생성
ko_cv.fit(ko_text)

## 생성된 단어 사전 확인: 인덱스는 등장 순서가 아니라 가나다순
ko_vocab = ko_cv.vocabulary_
print(f"생성된 단어 사전: \n{ko_vocab}")

## transform(): 사전을 기준으로 임베딩 행렬 생성
ko_embedding = ko_cv.transform(["나는 배가 고프다"]).toarray()
print(f"임베딩의 결과: \n{ko_embedding}")

# 6. 코사인 유사도

## 필요한 함수 임포트
from sklearn.metrics.pairwise import cosine_similarity

## 같은 사전으로 두 문장을 임베딩한 뒤 비교
ko_sim = cosine_similarity(ko_embedding1, ko_embedding2)
print(f"한글 문장 간의 코사인 유사도: {ko_sim}")

# 7. 영화 추천 서비스

## 필요한 컬럼만 팬시 인덱싱
df1 = df[["overview", "title"]]

## 누락 데이터 처리: 줄거리가 없으면 비교가 불가능하므로 삭제
df2 = df1.dropna(ignore_index=True)

## 데이터 축소: 서로 비교하므로 행렬 크기가 영화 수의 제곱이 됨
df3 = df2[0:10000]

## 임베딩: stop_words 설정으로 영어 불용어 자동 제거
cv = CountVectorizer(stop_words="english")

text_list = df3["overview"].tolist()
cv.fit(text_list)
embedding_matrix = cv.transform(text_list).toarray()

## 모든 영화끼리 비교 -> (10000, 10000) 행렬
sim = cosine_similarity(embedding_matrix, embedding_matrix)

## 숫자 행렬에 제목을 입혀 읽을 수 있게 만들기
df_sim = pd.DataFrame(
    data=sim,
    index=df3["title"].values,
    columns=df3["title"].values,
)

## 추천 함수 생성
def top_n_recommend(k, title):
    ### 사용자의 입력이 1만 편 목록에 있는 경우에만 실행
    if title in df_sim.columns:
        #### 1순위는 언제나 자기 자신이므로 한 칸 건너뜀
        top_n = df_sim[title].sort_values(ascending=False)[1 : k + 1]
        return top_n
    else:
        print("존재하지 않는 영화 제목이오니, 확인 후 다시 입력을 해주세요")

# 8. IMDB 감성 분석 데이터 준비

## 필요한 라이브러리 임포트
import numpy as np
import torch
from torch.utils.data import TensorDataset, DataLoader
import tensorflow as tf

## 연산 디바이스 설정
if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")

## 데이터 다운로드: 단어 사전 크기 10000
(X_train_raw, y_train_raw), (X_test, y_test) = tf.keras.datasets.imdb.load_data(
    num_words=10000
)

## 리뷰별 토큰 수 추출
token_length = []
for review in X_train_raw:
    length = len(review)
    token_length.append(length)

## 토큰 수 통계 분석: 분위수로 적절한 길이 찾기
stats = np.percentile(a=token_length, q=[75, 90, 100])
print(f"리뷰 토큰 수 분위수: \n{stats}")

## 리뷰 길이 균일화: 90분위수(467)를 근거로 470 설정
max_len = 470

X_train_pad = tf.keras.utils.pad_sequences(sequences=X_train_raw, maxlen=max_len)
X_test_pad = tf.keras.utils.pad_sequences(sequences=X_test, maxlen=max_len)

print(f"학습용 데이터의 모양: {X_train_pad.shape}")

## PyTorch Tensor 변환
"""
X 데이터: 단어 사전상의 정수 인덱스 -> 정수형(LongTensor)
y 데이터: 이진 분류의 예측값과 연산 가능해야 함 -> 실수형(FloatTensor)
"""
X_train_tensor = torch.LongTensor(X_train_pad).to(device)
y_train_tensor = torch.FloatTensor(y_train_raw).to(device)
X_test_tensor = torch.LongTensor(X_test_pad).to(device)
y_test_tensor = torch.FloatTensor(y_test).to(device)

## 문제와 정답을 쌍으로 묶기
train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
test_dataset = TensorDataset(X_test_tensor, y_test_tensor)

## 데이터 공급 장치 생성
train_loader = DataLoader(train_dataset, batch_size=250, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=250, shuffle=False)

# 9. 행렬 간의 곱셈

## 2차원 배열(행렬) 생성
matrix1 = np.array([[1, 2, 3],
                    [4, 5, 6]])
matrix2 = np.array([[1, 2],
                    [3, 4],
                    [5, 6]])

print(f"matrix1의 모양: {matrix1.shape}")
print(f"matrix2의 모양: {matrix2.shape}")

## 행렬 곱셈: (2, 3) x (3, 2) -> (2, 2)
output = np.matmul(matrix1, matrix2)
print(f"행렬 간 곱셈의 결과: \n{output}")

## 모양이 맞지 않으면 에러 발생: (2, 3) x (2, 2)
matrix3 = np.array([[1, 2],
                    [3, 4]])
output = np.matmul(matrix1, matrix3)   # ValueError