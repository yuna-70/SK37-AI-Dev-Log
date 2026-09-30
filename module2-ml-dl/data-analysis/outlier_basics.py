"""TIL: 이상치 처리 (2026-09-30) — 개념 설명은 README.md 참고"""

# 필요한 라이브러리 임포트
import pandas as pd

# 데이터 불러오기

## 파일 경로 설정
file_path = "weather.csv"

## DataFrame 생성
df_weather = pd.read_csv(file_path)

## 결과 확인
display(df_weather)

# 각 컬럼별 Q1, Q3, IQR 계산

## 각 컬럼별 Q1 계산 -> 25% 지점
q1 = df_weather.quantile(q=0.25)
print(f"각 컬럼별 1사분위 값 q1: \n{q1}")

print("-" * 80)

## 각 컬럼별 Q3 계산 -> 75% 지점
q3 = df_weather.quantile(q=0.75)
print(f"각 컬럼별 3사분위 값 q3: \n{q3}")

print("-" * 80)

## 각 컬럼별 IQR 계산 -> Q3 - Q1
iqr = q3 - q1
print(f"각 컬럼별 iqr: \n{iqr}")

# 각 컬럼별 정상 범위 최소값 / 최대값 계산

## 각 컬럼별 정상 범위의 최소값 -> Q1 - (1.5 * IQR)
min_val = q1 - (iqr * 1.5)
print(f"각 컬럼별 정상 범위의 최소값: \n{min_val}")

print("-" * 80)

## 각 컬럼별 정상 범위의 최대값 -> Q3 + (1.5 * IQR)
max_val = q3 + (iqr * 1.5)
print(f"각 컬럼별 정상 범위의 최대값: \n{max_val}")

# 데이터프레임 전체에 대해서 논리 연산자 적용 -> 이상치 여부 판단 -> 불리언 데이터 생성
df_outlier_bool = (df_weather < min_val) | (df_weather > max_val)
print(f"각 컬럼별 이상치의 유무: \n{df_outlier_bool}")

print("-" * 80)

# 행 별 이상치 유무 식별: 어떤 컬럼에서든 이상치가 하나라도 있는 행 -> True 표시 -> any(axis=1)
has_outlier = df_outlier_bool.any(axis=1)
print(f"행 별 이상치의 유무: \n{has_outlier}")

print("-" * 80)

# has_outlier -> 논리 부정(~) 적용 -> 정상 데이터인 행 = True
output = ~has_outlier
print(f"행 별 이상치 유무의 결과에 대해 논리 부정 적용: \n{output}")

print("-" * 80)

# 값 추출 -> Series.values -> 불리언 값으로 구성된 1차원 넘파이 배열(array)
arr_bool = output.values
print(f"불리언 값으로 구성된 1차원 배열: \n{arr_bool}")

print("-" * 80)

# 불리언 인덱싱: 불리언 값으로 구성된 배열을 이용한 인덱싱 -> True에 해당하는 행 추출
df_normal = df_weather[arr_bool]
print(f"정상인 데이터로만 구성된 데이터프레임: \n{df_normal}")

print("-" * 80)

# 이상치 대체: 삭제 대신 정상 범위의 경계값으로 일괄 변경 -> clip()
df_clipped = df_weather.clip(lower=min_val, upper=max_val, axis=1)
print(f"이상치를 경계값으로 대체한 데이터프레임: \n{df_clipped}")