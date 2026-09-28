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

# 수집 대상 목록 페이지를 지정합니다.
LIST_URL = "https://en.wikipedia.org/wiki/List_of_most-visited_museums"
# Wikipedia가 요청 주체를 식별할 수 있도록 User-Agent를 지정합니다.
HEADERS = {"User-Agent": "mini3-museum-collector/1.0 (educational project)"}
# 스크립트 파일이 있는 폴더를 기준으로 CSV 저장 경로를 지정합니다.
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "data" / "raw_p1.csv"
# 목록 페이지에 한 번만 요청합니다.
response = requests.get(LIST_URL, headers=HEADERS, timeout=30)
# 페이지가 알려 준 인코딩을 우선 적용하고 없으면 추정 인코딩을 적용합니다.
response.encoding = response.encoding or response.apparent_encoding
# 응답 HTML을 BeautifulSoup으로 분석합니다.
soup = BeautifulSoup(response.text, "html.parser")
# 페이지의 첫 번째 wikitable만 대상으로 삼습니다.
table = soup.select_one("table.wikitable")
# 첫 번째 표의 헤더 이름을 읽습니다.
header_cells = table.select_one("tr").find_all(["td", "th"]) if table is not None else []
# 헤더 글자를 소문자 목록으로 정리합니다.
header_names = [cell.get_text(" ", strip=True).lower() for cell in header_cells]
# 실제 표의 열 위치를 헤더 이름으로 찾습니다.
name_index = header_names.index("name")
# 실제 표의 방문객 수 열 위치를 찾습니다.
visitors_index = header_names.index("visitors")
# 실제 표의 도시 열 위치를 찾습니다.
city_index = header_names.index("city")
# 실제 표의 국가 열 위치를 찾습니다.
country_index = header_names.index("country")
# 수집 시점을 한국 시간으로 기록합니다.
scraped_at = datetime.now(ZoneInfo("Asia/Seoul")).isoformat(timespec="seconds")
# CSV 열 이름과 순서를 고정합니다.
columns = ["name", "city_raw", "country_raw", "visitors_raw", "detail_url", "scraped_at"]
# 파싱한 행을 담을 목록을 만듭니다.
rows = []
# 화면에 보이는 이름과 CSV 이름이 다른 항목 수를 셉니다.
truncated_name_count = 0
# 첫 번째 표가 있으면 표의 각 본문 행을 순서대로 확인합니다.
if table is not None:
    # 표의 모든 행에서 헤더 행은 제외하고 처리합니다.
    for tr in table.select("tr"):
        # 현재 행의 셀을 가져옵니다.
        cells = tr.find_all(["td", "th"])
        # 셀이 네 개보다 적으면 제목 또는 빈 행으로 보고 건너뜁니다.
        if len(cells) < 4 or any(cell.name == "th" for cell in cells):
            continue
        # 박물관 이름 셀에서 연결된 링크를 찾습니다.
        name_link = cells[name_index].find("a", href=True)
        # 화면에 보이는 이름 셀 전체의 텍스트를 추출합니다.
        visible_name = cells[name_index].get_text(" ", strip=True)
        # 박물관 이름과 전체 상세 URL을 추출합니다.
        name = name_link.get_text(" ", strip=True) if name_link else cells[name_index].get_text(" ", strip=True)
        # 화면 이름과 CSV에 저장할 이름이 다르면 개수를 하나 늘립니다.
        if visible_name != name:
            truncated_name_count += 1
        # 박물관 이름 링크를 https로 시작하는 전체 주소로 변환합니다.
        detail_url = urljoin(LIST_URL, name_link["href"]) if name_link else ""
        # 상대 링크가 남아 있으면 안전하게 전체 HTTPS 주소로 맞춥니다.
        if detail_url.startswith("http://"):
            detail_url = "https://" + detail_url[len("http://"):]
        # 화면에 보이는 도시 이름을 그대로 추출합니다.
        city_raw = cells[city_index].get_text(" ", strip=True)
        # 화면에 보이는 국가 이름을 그대로 추출합니다.
        country_raw = cells[country_index].get_text(" ", strip=True)
        # 화면에 보이는 방문객 수 글자를 그대로 추출합니다.
        visitors_raw = cells[visitors_index].get_text(" ", strip=True)
        # 추출한 값을 지정된 열 순서로 추가합니다.
        rows.append({"name": name, "city_raw": city_raw, "country_raw": country_raw, "visitors_raw": visitors_raw, "detail_url": detail_url, "scraped_at": scraped_at})
# 응답 상태 코드와 수집 행 수를 출력합니다.
print(f"응답 상태 코드: {response.status_code}")
# 수집된 전체 행 수를 출력합니다.
print(f"수집 행 수: {len(rows)}")
# 화면 이름과 CSV 이름이 다른 항목 수를 출력합니다.
print(f"잘려 보이는 이름: {truncated_name_count}개")
# 앞 3행을 pandas 표 형식으로 출력합니다.
preview = pd.DataFrame(rows, columns=columns).head(3)
# 앞 3행을 출력합니다.
print(preview)
# 응답이 정상이고 행이 있을 때만 CSV를 저장합니다.
if response.status_code == 200 and rows:
    # 지정된 열 순서와 UTF-8 BOM 인코딩으로 CSV를 저장합니다.
    pd.DataFrame(rows, columns=columns).to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
