# CSV 파일을 읽고 표를 다루기 위해 pandas를 불러옵니다.
import pandas as pd
# 정규 표현식으로 숫자 부분을 뽑기 위해 re를 불러옵니다.
import re
# 스크립트 위치 기준 경로를 만들기 위해 Path를 불러옵니다.
from pathlib import Path

# 스크립트 파일 위치를 기준으로 원본 CSV 경로를 지정합니다.
RAW_PATH = Path(__file__).resolve().parent.parent / "data" / "raw.csv"
# 스크립트 파일 위치를 기준으로 정제 CSV 경로를 지정합니다.
CLEAN_PATH = Path(__file__).resolve().parent.parent / "data" / "clean.csv"
# 원본 CSV를 문자열 그대로 읽습니다.
raw = pd.read_csv(RAW_PATH, encoding="utf-8-sig", dtype=object)
# 원본의 행별 제외 사유를 담을 목록을 만듭니다.
excluded = []
# 원본 열을 유지한 채 복사본을 만듭니다.
clean = raw.copy()
# 실제 Wikipedia 표에서 방문객 수로 저장된 city_raw의 앞쪽 숫자를 추출합니다.
visitor_text = clean["city_raw"].astype("string").str.extract(r"^\s*([0-9,]+)", expand=False).str.replace(",", "", regex=False)
# 추출한 방문객 수를 숫자형 새 열 visitors로 만듭니다.
clean["visitors"] = pd.to_numeric(visitor_text, errors="coerce").astype("Int64")
# 실제 Wikipedia 표에서 도시로 저장된 country_raw의 앞뒤 공백을 정리해 city를 만듭니다.
clean["city"] = clean["country_raw"].astype("string").str.strip()
# 실제 Wikipedia 표에서 국가로 저장된 visitors_raw의 앞뒤 공백을 정리해 country를 만듭니다.
clean["country"] = clean["visitors_raw"].astype("string").str.strip()
# 숫자로 바뀌지 않은 원문을 찾습니다.
bad_visitors = clean["visitors"].isna()
# 숫자로 바뀌지 않은 값과 행 번호를 출력합니다.
for index in clean.index[bad_visitors]:
    print(f"제외 예정 행 {index}: city_raw 방문객 수 변환 실패 -> {raw.loc[index, 'city_raw']!r}")
# name, visitors, detail_url 중 빈칸인 행을 찾습니다.
missing = clean[["name", "visitors", "detail_url"]].isna().any(axis=1) | clean[["name", "detail_url"]].eq("").any(axis=1)
# 빈칸 행의 사유를 출력합니다.
for index in clean.index[missing & ~bad_visitors]:
    print(f"제외 예정 행 {index}: 필수 값 빈칸")
# detail_url 중복 행을 찾습니다.
duplicate_url = clean["detail_url"].duplicated(keep="first")
# 중복 URL 행의 사유를 출력합니다.
for index in clean.index[duplicate_url & ~bad_visitors & ~missing]:
    print(f"제외 예정 행 {index}: detail_url 중복 -> {clean.loc[index, 'detail_url']}")
# 변환 실패·필수 값 빈칸·중복 URL 행을 제거합니다.
drop_rows = bad_visitors | missing | duplicate_url
# 문제가 있는 행을 새 표에서 제외합니다.
clean = clean.loc[~drop_rows].copy()
# 정제된 표를 지정한 인코딩으로 저장합니다.
clean.to_csv(CLEAN_PATH, index=False, encoding="utf-8-sig")
# 처리 전후의 행 수를 출력합니다.
print(f"행 수: 처리 전 {len(raw)} · 처리 후 {len(clean)}")
# 처리 전후의 데이터형을 출력합니다.
print(f"데이터형: 처리 전 city_raw={raw['city_raw'].dtype}, 처리 후 visitors={clean['visitors'].dtype}")
# 처리 전후의 열별 빈칸 수를 출력합니다.
print(f"빈칸 수: 처리 전 {int(raw.isna().sum().sum())} · 처리 후 {int(clean.isna().sum().sum())}")
# 처리 전후의 detail_url 중복 수를 출력합니다.
print(f"detail_url 중복 수: 처리 전 {int(raw['detail_url'].duplicated().sum())} · 처리 후 {int(clean['detail_url'].duplicated().sum())}")
# 제외된 행 수를 출력합니다.
print(f"제외 행 수: {int(drop_rows.sum())}")
