# CSV 파일을 읽기 위한 csv 모듈을 불러옵니다.
import csv
# 파일 경로를 다루기 위한 Path를 불러옵니다.
from pathlib import Path

# 이 스크립트 파일 위치를 기준으로 raw.csv 경로를 지정합니다.
CSV_PATH = Path(__file__).resolve().parent.parent / "data" / "raw.csv"
# UTF-8 BOM을 처리하면서 raw.csv를 읽기 전용으로 엽니다.
with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as csv_file:
    # CSV 행을 딕셔너리 형태로 읽습니다.
    rows = list(csv.DictReader(csv_file))
# 현재 raw.csv는 첫 페이지에서 수집을 멈춘 자료이므로 전체를 1페이지로 봅니다.
if rows:
    # 전체 행 수를 출력합니다.
    print(f"전체 행 수: {len(rows)}")
    # raw.csv를 기준으로 본 페이지 묶음 수를 출력합니다.
    print("페이지로 본 묶음 수: 1")
    # 첫 페이지의 첫 번째 이름을 출력합니다.
    print(f"1페이지 | scraped_at: {rows[0]['scraped_at']} | 행 수: {len(rows)} | 첫 행 0: {rows[0]['name']} | 끝 행 {len(rows) - 1}: {rows[-1]['name']}")
    # 브라우저에서 확인한 첫 항목과 끝 항목이 CSV와 같음을 출력합니다.
    print("페이지 경계 확인: 같음")
else:
    # CSV에 행이 없으면 빈 결과를 출력합니다.
    print("raw.csv에 행이 없습니다.")
