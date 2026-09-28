# 정제 CSV를 읽고 JSON으로 내보내기 위해 pandas를 불러옵니다.
import pandas as pd
# JSON 파일을 쓰기 위해 json을 불러옵니다.
import json
# 파일 경로를 다루기 위해 Path를 불러옵니다.
from pathlib import Path

# 스크립트 위치를 기준으로 clean.csv 경로를 지정합니다.
CLEAN_PATH = Path(__file__).resolve().parent.parent / "data" / "clean.csv"
# 스크립트 위치를 기준으로 data.json 경로를 지정합니다.
JSON_PATH = Path(__file__).resolve().parent.parent / "data" / "data.json"
# 정제 CSV를 읽습니다.
clean = pd.read_csv(CLEAN_PATH, encoding="utf-8-sig")
# 웹 화면에 필요한 열만 선택합니다.
web_columns = ["name", "city", "visitors", "detail_url"]
# 선택한 열을 행별 딕셔너리 목록으로 바꿉니다.
records = clean[web_columns].to_dict(orient="records")
# JSON을 UTF-8로 사람이 읽기 좋게 저장합니다.
with JSON_PATH.open("w", encoding="utf-8") as json_file:
    # 한글을 그대로 쓰고 들여쓰기를 적용합니다.
    json.dump(records, json_file, ensure_ascii=False, indent=2)
# 저장한 JSON을 다시 읽습니다.
with JSON_PATH.open("r", encoding="utf-8") as json_file:
    # JSON 목록을 다시 불러옵니다.
    saved_records = json.load(json_file)
# JSON 항목 수와 정제 행 수를 비교해 출력합니다.
print(f"항목 수: {len(saved_records)} · 정제 행 수: {len(clean)} · {'같음' if len(saved_records) == len(clean) else '다름'}")
# JSON 첫 항목을 출력합니다.
print("data.json 첫 항목:")
print(saved_records[0])
# 정제 CSV 첫 줄의 웹 열을 출력합니다.
print("clean.csv 첫 줄:")
print(clean.loc[0, web_columns].to_dict())
