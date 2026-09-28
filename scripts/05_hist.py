# 정제 CSV를 읽고 구간별 빈도를 계산하기 위해 pandas를 불러옵니다.
import pandas as pd
# 히스토그램 구간과 빈도를 계산하기 위해 numpy를 불러옵니다.
import numpy as np
# 파일 경로를 다루기 위해 Path를 불러옵니다.
from pathlib import Path
# 화면 창 없이 파일로 저장하는 matplotlib 백엔드를 지정합니다.
import matplotlib
# 비대화형 Agg 백엔드를 사용합니다.
matplotlib.use("Agg")
# 히스토그램을 그리기 위해 matplotlib의 pyplot을 불러옵니다.
import matplotlib.pyplot as plt
# 가로축 눈금의 표시 형식을 바꾸기 위해 포매터를 불러옵니다.
from matplotlib.ticker import FuncFormatter

# 스크립트 파일 위치를 기준으로 clean.csv 경로를 지정합니다.
CLEAN_PATH = Path(__file__).resolve().parent.parent / "data" / "clean.csv"
# 스크립트 파일 위치를 기준으로 그림 저장 폴더를 지정합니다.
CHART_PATH = Path(__file__).resolve().parent.parent / "charts" / "hist.png"
# 정제 CSV를 읽습니다.
clean = pd.read_csv(CLEAN_PATH, encoding="utf-8-sig")
# 실제 숫자 열인 city를 사용합니다.
values = clean["city"].to_numpy()
# 최솟값과 최댓값을 감싸는 둥근 구간 경계를 고정합니다.
bins = np.arange(1_000_000, 10_000_001, 1_000_000)
# 마지막 구간의 오른쪽 끝을 포함하는 빈도를 계산합니다.
frequencies, edges = np.histogram(values, bins=bins)
# 그림 크기를 지정합니다.
fig, ax = plt.subplots(figsize=(10, 6))
# 히스토그램 막대를 그립니다.
ax.hist(values, bins=bins, edgecolor="black", align="left", rwidth=0.98)
# 막대 위에 각 구간의 개수를 표시합니다.
for left, right, frequency in zip(edges[:-1], edges[1:], frequencies):
    # 빈도가 0인 막대도 구간별로 표시합니다.
    ax.text((left + right) / 2, frequency + 0.2, str(int(frequency)), ha="center", va="bottom")
# 가로축 이름을 영어로 지정합니다.
ax.set_xlabel("Visitors (people)")
# 세로축 이름을 영어로 지정합니다.
ax.set_ylabel("Number of museums")
# 제목에 정제 행 수를 넣습니다.
ax.set_title(f"Most-visited museums distribution, n = {len(clean)}")
# 가로축 눈금을 구간 경계로 지정합니다.
ax.set_xticks(bins)
# 가로축 눈금을 백만 단위의 영어 표기로 지정합니다.
ax.xaxis.set_major_formatter(FuncFormatter(lambda value, position: f"{value / 1_000_000:.0f}M"))
# 눈금 글자가 겹치지 않도록 회전합니다.
ax.tick_params(axis="x", labelrotation=45)
# 그림 여백을 자동으로 정리합니다.
fig.tight_layout()
# 그림을 파일로 저장합니다.
fig.savefig(CHART_PATH, dpi=150)
# 그림 창은 띄우지 않습니다.
plt.close(fig)
# 구간별 빈도 표를 출력합니다.
print("| 구간 | 개수 |\n|---|---:|")
# 각 구간의 경계와 빈도를 출력합니다.
for index, frequency in enumerate(frequencies):
    # 마지막 구간만 오른쪽 끝을 포함한다고 표시합니다.
    if index == len(frequencies) - 1:
        label = f"{edges[index]:,.0f} 이상 {edges[index + 1]:,.0f} 이하"
    else:
        label = f"{edges[index]:,.0f} 이상 {edges[index + 1]:,.0f} 미만"
    # 현재 구간의 빈도를 출력합니다.
    print(f"| {label} | {int(frequency)} |")
# 빈도 합과 정제 행 수가 같은지 출력합니다.
print(f"| **합계** | **{int(frequencies.sum())} = 정제 행 수 {len(clean)}** |")
print(f"빈도 합: {int(frequencies.sum())} · 정제 행 수: {len(clean)} · {'같음' if frequencies.sum() == len(clean) else '다름'}")
