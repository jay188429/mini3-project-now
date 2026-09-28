# HTTP 요청을 보내기 위한 requests를 불러옵니다.
import requests
# HTML을 분석하기 위한 BeautifulSoup을 불러옵니다.
from bs4 import BeautifulSoup
# 표를 만들고 CSV로 저장하기 위한 pandas를 불러옵니다.
import pandas as pd
# 상대 링크를 전체 URL로 바꾸기 위한 함수를 불러옵니다.
from urllib.parse import urljoin
# 한국 시간대의 수집 시각을 만들기 위한 도구를 불러옵니다.
from datetime import datetime
# 시간대를 다루기 위한 표준 라이브러리를 불러옵니다.
from zoneinfo import ZoneInfo
# 스크립트 파일 위치를 기준으로 경로를 만들기 위한 도구를 불러옵니다.
from pathlib import Path

# M02에서 사용한 Wikipedia 목록 페이지를 지정합니다.
LIST_URL = "https://en.wikipedia.org/wiki/List_of_most-visited_museums"
# Wikipedia가 요청 주체를 식별할 수 있도록 User-Agent를 지정합니다.
HEADERS = {"User-Agent": "mini3-museum-collector/1.0 (educational project)"}
# 스크립트 파일 위치를 기준으로 원본 CSV 저장 경로를 지정합니다.
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "raw.csv"
# CSV 열 이름과 순서를 M02와 같게 지정합니다.
COLUMNS = ["name", "city_raw", "country_raw", "visitors_raw", "detail_url", "scraped_at"]
# 합친 행을 담을 목록을 만듭니다.
all_rows = []
# 페이지별 수집을 시작합니다.
for page_number in range(1, 4):
    # 첫 페이지에서 50행 이상을 얻으므로 이 페이지 하나만 요청합니다.
    if page_number > 1:
        # 목표 행 수에 도달하면 추가 페이지를 요청하지 않습니다.
        break
    # 목록 페이지를 한 번 요청합니다.
    response = requests.get(LIST_URL, headers=HEADERS, timeout=30)
    # 페이지가 알려 준 인코딩을 우선 사용하고 없으면 추정 인코딩을 사용합니다.
    response.encoding = response.encoding or response.apparent_encoding
    # 응답 HTML을 BeautifulSoup으로 분석합니다.
    soup = BeautifulSoup(response.text, "html.parser")
    # 첫 번째 wikitable만 대상으로 삼습니다.
    table = soup.select_one("table.wikitable")
    # 현재 페이지의 수집 시각을 한국 시간으로 기록합니다.
    scraped_at = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")
    # 현재 페이지의 행을 담을 목록을 만듭니다.
    page_rows = []
    # 첫 번째 표가 있으면 표의 각 행을 확인합니다.
    if table is not None:
        # 표의 행을 순서대로 처리합니다.
        for tr in table.select("tr"):
            # 현재 행의 셀을 가져옵니다.
            cells = tr.find_all(["td", "th"])
            # 헤더나 셀이 부족한 행은 건너뜁니다.
            if len(cells) < 4 or any(cell.name == "th" for cell in cells):
                continue
            # 박물관 이름 셀에서 연결된 링크를 찾습니다.
            name_link = cells[0].find("a", href=True)
            # 박물관 이름을 화면에 보이는 링크 텍스트 그대로 추출합니다.
            name = name_link.get_text(" ", strip=True) if name_link else cells[0].get_text(" ", strip=True)
            # 박물관 이름 링크를 전체 HTTPS 주소로 변환합니다.
            detail_url = urljoin(LIST_URL, name_link["href"]) if name_link else ""
            # HTTP로 시작하는 링크는 HTTPS로 맞춥니다.
            if detail_url.startswith("http://"):
                detail_url = "https://" + detail_url[len("http://"):]
            # 두 번째 셀의 글자를 그대로 저장합니다.
            city_raw = cells[1].get_text(" ", strip=True)
            # 세 번째 셀의 글자를 그대로 저장합니다.
            country_raw = cells[2].get_text(" ", strip=True)
            # 네 번째 셀의 글자를 그대로 저장합니다.
            visitors_raw = cells[3].get_text(" ", strip=True)
            # 현재 행을 지정한 열 순서로 추가합니다.
            page_rows.append({"name": name, "city_raw": city_raw, "country_raw": country_raw, "visitors_raw": visitors_raw, "detail_url": detail_url, "scraped_at": scraped_at})
    # 페이지 주소와 응답 상태와 행 수를 출력합니다.
    print(f"{LIST_URL}  {response.status_code}  {len(page_rows)}행")
    # 응답 상태가 정상이 아니면 수집을 멈춥니다.
    if response.status_code != 200:
        print(f"{page_number}페이지에서 멈춤")
        break
    # 페이지 행 수가 0이면 수집을 멈춥니다.
    if len(page_rows) == 0:
        print(f"{page_number}페이지에서 멈춤")
        break
    # 현재 페이지 행을 전체 행에 이어 붙입니다.
    all_rows.extend(page_rows)
    # 50행 이상이면 목표에 도달했으므로 멈춥니다.
    if len(all_rows) >= 50:
        break
    # 다음 페이지 요청 전에는 1초 쉽니다.
    import time
    time.sleep(1)
# 전체 행으로 pandas 표를 만듭니다.
result = pd.DataFrame(all_rows, columns=COLUMNS)
# 응답 상태가 정상이고 행이 있으면 원본 CSV를 저장합니다.
if all_rows and len(all_rows) >= 50:
    # 원본 값을 바꾸지 않고 UTF-8 BOM 형식으로 저장합니다.
    result.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
# 합계 행 수와 서로 다른 상세 주소 수를 출력합니다.
print(f"합계 {len(result)}행 · 서로 다른 detail_url {result['detail_url'].nunique()}개")
# 표본 행 번호를 계산합니다.
sample_indexes = [0, len(result) // 2, len(result) - 1]
# 표본 3행을 모든 열과 함께 출력합니다.
for index in sample_indexes:
    # 표본 행 번호와 값을 출력합니다.
    print(f"행 {index}")
    print(result.iloc[index].to_string())
