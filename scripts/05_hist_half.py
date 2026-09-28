# 정제 CSV를 읽고 반 구간 히스토그램을 만들기 위해 pandas를 불러옵니다.
import pandas as pd
# 구간과 빈도를 계산하기 위해 numpy를 불러옵니다.
import numpy as np
# 파일 경로를 다루기 위해 Path를 불러옵니다.
from pathlib import Path
# 화면 없이 그림을 파일로 저장하기 위한 matplotlib 백엔드를 지정합니다.
import matplotlib
# 비대화형 백엔드를 사용합니다.
matplotlib.use("Agg")
# 히스토그램을 그리기 위해 pyplot을 불러옵니다.
import matplotlib.pyplot as plt
# 가로축 눈금 형식을 지정하기 위해 포매터를 불러옵니다.
from matplotlib.ticker import FuncFormatter

# 스크립트 위치를 기준으로 clean.csv 경로를 지정합니다.
CLEAN_PATH = Path(__file__).resolve().parent.parent / "data" / "clean.csv"
# 기존 hist.png를 덮어쓰지 않는 새 그림 경로를 지정합니다.
CHART_PATH = Path(__file__).resolve().parent.parent / "charts" / "hist_half.png"
# 정제 CSV를 읽습니다.
clean = pd.read_csv(CLEAN_PATH, encoding="utf-8-sig")
# 실제 숫자 열인 city를 사용합니다.
values = clean["city"].to_numpy()
# 기존 폭의 절반인 500,000 단위의 경계를 지정합니다.
bins = np.arange(1_000_000, 10_000_001, 500_000)
# 마지막 경계를 포함하는 구간별 빈도를 계산합니다.
frequencies, edges = np.histogram(values, bins=bins)
# 그림을 만듭니다.
fig, ax = plt.subplots(figsize=(10, 6))
# 반으로 줄인 구간 폭으로 막대를 그립니다.
ax.hist(values, bins=bins, edgecolor="black", align="left", rwidth=0.98)
# 각 막대 위에 빈도를 표시합니다.
for left, right, frequency in zip(edges[:-1], edges[1:], frequencies):
    # 빈도가 0인 구간도 표시합니다.
    ax.text((left + right) / 2, frequency + 0.2, str(int(frequency)), ha="center", va="bottom")
# 가로축 이름을 영어로 지정합니다.
ax.set_xlabel("Visitors (people)")
# 세로축 이름을 영어로 지정합니다.
ax.set_ylabel("Number of museums")
# 제목에 정제 행 수를 넣습니다.
ax.set_title(f"Most-visited museums distribution, half-width bins, n = {len(clean)}")
# 백만 단위 경계에 눈금을 표시합니다.
ax.set_xticks(np.arange(1_000_000, 10_000_001, 1_000_000))
# 눈금을 백만 단위 영어 표기로 표시합니다.
ax.xaxis.set_major_formatter(FuncFormatter(lambda value, position: f"{value / 1_000_000:.0f}M"))
# 그림 여백을 정리합니다.
fig.tight_layout()
# 기존 그림과 다른 파일로 저장합니다.
fig.savefig(CHART_PATH, dpi=150)
# 그림 창을 띄우지 않습니다.
plt.close(fig)
# 가장 높은 막대의 위치를 찾습니다.
maximum_index = int(np.argmax(frequencies))
# 가장 높은 막대의 구간과 빈도를 출력합니다.
print(f"가장 높은 막대: {edges[maximum_index]:,.0f} 이상 {edges[maximum_index + 1]:,.0f} 미만 · {int(frequencies[maximum_index])}개")
# 반 폭 구간의 빈도 합과 정제 행 수를 출력합니다.
print(f"빈도 합: {int(frequencies.sum())} · 정제 행 수: {len(clean)} · {'같음' if frequencies.sum() == len(clean) else '다름'}")
