# LUMEN ATLAS

방문객 수와 국가를 입력하면 조건에 맞는 미술관 후보를 보여 주고, 후보 안에서 AI가 한 곳을 추천하는 서비스입니다.

배포 주소 : https://world-museum-atlas.vercel.app

## 실행 안내

이 `README.md`와 `index.html`이 들어 있는 저장소 최상위 폴더에서 터미널을 엽니다.

### 1. 다시 모으기

| 순서 | 파일 | 만드는 것 | 명령 | 확인 |
|---:|---|---|---|---|
| 1 | `scripts/02_collect.py` | `data/raw.csv` · 목록 수집 | `python scripts/02_collect.py` | 확인 안 함 |
| 2 | `scripts/03_clean.py` | `data/clean.csv` · 방문객 수 정제 | `python scripts/03_clean.py` | 확인 안 함 |
| 3 | `scripts/05_hist.py` | `charts/hist.png` · 방문객 수 히스토그램 | `python scripts/05_hist.py` | 확인 안 함 |
| 4 | `scripts/06_by_category.py` | `charts/by_category.png` · 국가별 평균 차트 | `python scripts/06_by_category.py` | 확인 안 함 |
| 5 | `scripts/07_export_json.py` | `data/data.json` · 화면용 데이터 | `python scripts/07_export_json.py` | 확인 안 함 |

- `02_collect.py`는 수집 사이트에 요청을 보냅니다. 페이지 수를 임의로 늘리지 않습니다.
- macOS/Linux에서는 `python` 대신 `python3`를 사용합니다.
- 모든 명령은 위 표의 순서대로 저장소 최상위 폴더에서 실행합니다.

### 2. 화면에 반영하기

새로 만든 `data/data.json`과 `charts/` 파일을 확인한 뒤 커밋하고 GitHub에 푸시합니다. Vercel이 연결된 저장소의 새 커밋을 감지하면 배포 주소를 다시 빌드합니다.

### 3. AI 연결

Vercel 프로젝트 환경변수에 이름 `GEMINI_API_KEY`를 추가하고 값을 넣습니다. 값을 코드·README·커밋에 기록하지 않습니다. 환경변수를 저장한 뒤 Redeploy를 실행합니다.

## 데이터와 보고서

- 원본·정제·웹용 데이터 : `data/raw.csv`, `data/clean.csv`, `data/data.json`
- 차트 : `charts/hist.png`, `charts/by_category.png`, `charts/country_average_visitors.png`, `charts/visitor_distribution_histogram.svg`
- 보고서 : `Mini project report.md`, `Mini project report.pdf`, `M21_report.md`, `M21_report.pdf`
