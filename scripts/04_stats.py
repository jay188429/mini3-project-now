# 정제 CSV를 읽고 통계를 계산하기 위해 pandas를 불러옵니다.
import pandas as pd
# 스크립트 위치 기준 경로를 만들기 위해 Path를 불러옵니다.
from pathlib import Path

# 스크립트 파일 위치를 기준으로 clean.csv 경로를 지정합니다.
CLEAN_PATH = Path(__file__).resolve().parent.parent / "data" / "clean.csv"
# 정제 CSV만 읽습니다.
clean = pd.read_csv(CLEAN_PATH, encoding="utf-8-sig")
# 통계를 계산할 실제 숫자 열을 지정합니다.
NUMBER_COLUMN = "visitors"
# 숫자 열의 값으로 통계를 계산합니다.
values = clean[NUMBER_COLUMN]
# 최소값 행을 찾습니다.
minimum_row = clean.loc[values.idxmin()]
# 최대값 행을 찾습니다.
maximum_row = clean.loc[values.idxmax()]
# 개수를 계산합니다.
count = int(values.count())
# 최소값을 계산합니다.
minimum = values.min()
# 최대값을 계산합니다.
maximum = values.max()
# 평균을 계산합니다.
mean = values.mean()
# 중앙값을 계산합니다.
median = values.median()
# 통계표를 출력합니다.
print("| 항목 | 값 |\n|---|---:|")
# 개수와 정제 행 수를 출력합니다.
print(f"| 개수 | {count} (정제 행 수 {len(clean)} · {'같음' if count == len(clean) else '다름'}) |")
# 최소값과 해당 행의 이름과 범주를 출력합니다.
print(f"| 최소 | {minimum} — {minimum_row['name']} · {minimum_row['country']} |")
# 최대값과 해당 행의 이름과 범주를 출력합니다.
print(f"| 최대 | {maximum} — {maximum_row['name']} · {maximum_row['country']} |")
# 평균을 소수 둘째 자리까지 출력합니다.
print(f"| 평균 | {mean:.2f} |")
# 중앙값을 계산된 값 그대로 출력합니다.
print(f"| 중앙값 | {median} |")
# 평균과 중앙값의 관계를 설명합니다.
if mean > median:
    print(f"평균 {mean:.2f}이 중앙값 {median}보다 큽니다.")
elif mean < median:
    print(f"평균 {mean:.2f}이 중앙값 {median}보다 작습니다.")
else:
    print(f"평균 {mean:.2f}과 중앙값 {median}이 같습니다.")
