# 정제 CSV를 읽고 범주별 중앙값을 계산하기 위해 pandas를 불러옵니다.
import pandas as pd
# 화면 없이 그림을 저장하기 위한 matplotlib 백엔드를 지정합니다.
import matplotlib
# 비대화형 백엔드를 사용합니다.
matplotlib.use("Agg")
# 막대그래프를 그리기 위해 pyplot을 불러옵니다.
import matplotlib.pyplot as plt
# 파일 경로를 다루기 위해 Path를 불러옵니다.
from pathlib import Path

# 스크립트 파일 위치를 기준으로 clean.csv 경로를 지정합니다.
CLEAN_PATH = Path(__file__).resolve().parent.parent / "data" / "clean.csv"
# 평균 그래프를 덮어쓰지 않을 중앙값 그래프 경로를 지정합니다.
CHART_PATH = Path(__file__).resolve().parent.parent / "charts" / "by_category_median.png"
# 정제 CSV만 읽습니다.
clean = pd.read_csv(CLEAN_PATH, encoding="utf-8-sig")
# 범주별 개수와 평균과 중앙값을 계산합니다.
summary = clean.groupby("country", sort=True)["visitors"].agg(["count", "mean", "median"]).reset_index()
# 범주 순서를 고정합니다.
positions = range(len(summary))
# 그림을 만듭니다.
fig, ax = plt.subplots(figsize=(14, 7))
# 범주별 중앙값 막대를 그립니다.
bars = ax.bar(positions, summary["median"])
# 막대 위에 중앙값과 n을 표시합니다.
for position, bar, median, count in zip(positions, bars, summary["median"], summary["count"]):
    # 중앙값과 표본 수를 두 줄로 표시합니다.
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{median:,.0f}\nn={int(count)}", ha="center", va="bottom", fontsize=8)
# 가로축에 범주 이름을 표시합니다.
ax.set_xticks(list(positions))
# 범주 이름이 겹치지 않도록 회전합니다.
ax.set_xticklabels(summary["country"], rotation=45, ha="right")
# 가로축 이름을 영어로 지정합니다.
ax.set_xlabel("Country category")
# 세로축 이름을 영어로 지정합니다.
ax.set_ylabel("Median visitors (people)")
# 제목에 전체 정제 행 수를 넣습니다.
ax.set_title(f"Median visitors by country category, n = {len(clean)}")
# 막대 위 글자를 위한 여백을 확보합니다.
ax.margins(y=0.15)
# 그림 여백을 자동으로 정리합니다.
fig.tight_layout()
# 중앙값 그래프를 별도 파일로 저장합니다.
fig.savefig(CHART_PATH, dpi=150)
# 그림 창을 띄우지 않습니다.
plt.close(fig)
# 중앙값 표를 출력합니다.
print("| 범주 | 개수 | 평균 | 중앙값 |\n|---|---:|---:|---:|")
# 각 범주의 평균과 중앙값을 출력합니다.
for _, row in summary.iterrows():
    # 현재 범주의 실제 값을 출력합니다.
    print(f"| {row['country']} | {int(row['count'])} | {row['mean']:.2f} | {row['median']:.2f} |")
# 평균 순위와 중앙값 순위를 계산합니다.
mean_order = summary.sort_values(["mean", "country"], ascending=[False, True])["country"].tolist()
# 중앙값 순위를 계산합니다.
median_order = summary.sort_values(["median", "country"], ascending=[False, True])["country"].tolist()
# 두 순위 목록을 출력합니다.
print(f"평균 순위: {' > '.join(mean_order)}")
print(f"중앙값 순위: {' > '.join(median_order)}")
# 순위가 달라진 범주를 출력합니다.
changed = [category for category in summary["country"] if mean_order.index(category) != median_order.index(category)]
# 순위 변화 범주를 출력합니다.
print(f"순위가 바뀐 그룹: {', '.join(changed) if changed else '없음'}")
