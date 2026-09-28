# 정제 데이터를 읽고 EDA 결과 카드를 만들기 위해 pandas를 불러옵니다.
import pandas as pd
# 구간별 빈도를 계산하기 위해 numpy를 불러옵니다.
import numpy as np
# 카드 이미지를 만들기 위해 matplotlib 백엔드를 지정합니다.
import matplotlib
# 화면 창 없이 파일로 저장합니다.
matplotlib.use("Agg")
# 그림을 그리기 위한 pyplot을 불러옵니다.
import matplotlib.pyplot as plt
# 카드 안의 여러 그림 배치를 위한 GridSpec을 불러옵니다.
from matplotlib.gridspec import GridSpec
# 파일 경로를 다루기 위해 Path를 불러옵니다.
from pathlib import Path

# 스크립트 위치를 기준으로 clean.csv 경로를 지정합니다.
CLEAN_PATH = Path(__file__).resolve().parent.parent / "data" / "clean.csv"
# 결과 카드 이미지 저장 경로를 지정합니다.
CARD_PATH = Path(__file__).resolve().parent.parent / "charts" / "eda_card.png"
# 정제 CSV를 읽습니다.
clean = pd.read_csv(CLEAN_PATH, encoding="utf-8-sig")
# 숫자 열을 가져옵니다.
values = clean["city"]
# 히스토그램 구간을 기존 M06과 동일하게 지정합니다.
hist_bins = np.arange(1_000_000, 10_000_001, 1_000_000)
# 히스토그램 빈도를 계산합니다.
hist_counts, _ = np.histogram(values, bins=hist_bins)
# 국가 범주별 평균과 개수를 계산합니다.
summary = clean.groupby("visitors", sort=True)["city"].agg(["count", "mean"]).reset_index()
# 카드 전체 그림과 두 개의 차트 영역을 만듭니다.
fig = plt.figure(figsize=(16, 12))
# 카드의 제목과 차트 배치를 지정합니다.
grid = GridSpec(3, 1, figure=fig, height_ratios=[0.4, 1.3, 1.7], hspace=0.45)
# 카드 제목을 표시합니다.
fig.suptitle("EDA Result Card — Most-visited museums", fontsize=20, fontweight="bold")
# 첫 번째 차트 영역을 만듭니다.
hist_ax = fig.add_subplot(grid[1, 0])
# 히스토그램 막대를 그립니다.
hist_ax.hist(values, bins=hist_bins, edgecolor="black", align="left", rwidth=0.98)
# 히스토그램 막대 위에 개수를 표시합니다.
for left, right, count in zip(hist_bins[:-1], hist_bins[1:], hist_counts):
    hist_ax.text((left + right) / 2, count + 0.2, str(int(count)), ha="center", va="bottom", fontsize=8)
# 히스토그램 축 이름과 제목을 지정합니다.
hist_ax.set_xlabel("Visitors (people)")
hist_ax.set_ylabel("Number of museums")
hist_ax.set_title("Q1. Where are visitor counts concentrated?", loc="left", fontsize=13)
# 히스토그램 눈금을 백만 단위로 표시합니다.
hist_ax.set_xticks(hist_bins)
hist_ax.set_xticklabels([f"{int(value / 1_000_000)}M" for value in hist_bins])
# 두 번째 차트 영역을 만듭니다.
category_ax = fig.add_subplot(grid[2, 0])
# 국가별 평균 막대를 그립니다.
bars = category_ax.bar(summary["visitors"], summary["mean"])
# 막대마다 평균과 n을 표시합니다.
for bar, mean, count in zip(bars, summary["mean"], summary["count"]):
    category_ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{mean:,.0f}\nn={int(count)}", ha="center", va="bottom", fontsize=7)
# 범주별 평균 차트의 축 이름과 제목을 지정합니다.
category_ax.set_xlabel("Country category")
category_ax.set_ylabel("Average visitors (people)")
category_ax.set_title("Q2. Do average visitor counts differ by country category?", loc="left", fontsize=13)
# 범주 이름이 겹치지 않도록 회전합니다.
category_ax.tick_params(axis="x", labelrotation=45)
# 카드 하단에 사실·추정·한계를 적습니다.
fig.text(0.05, 0.02, "Fact: 1M–2M has the most museums (29). Vatican average is highest (6,933,822); Brazil is lowest (1,364,208).\nLimit: one page, 72 rows; several categories have n=1. The charts show differences, not causes.", fontsize=10, va="bottom")
# 카드 전체 여백을 정리합니다.
fig.subplots_adjust(top=0.93, bottom=0.10, left=0.08, right=0.98)
# 결과 카드를 파일로 저장합니다.
fig.savefig(CARD_PATH, dpi=150)
# 그림 창을 띄우지 않습니다.
plt.close(fig)
# 저장 경로와 행 수를 출력합니다.
print(f"EDA 결과 카드 저장: {CARD_PATH}")
print(f"정제 행 수: {len(clean)}")
