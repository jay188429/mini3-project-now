# 정제 CSV를 읽고 그룹별 통계를 계산하기 위해 pandas를 불러옵니다.
import pandas as pd
# 파일 경로를 다루기 위해 Path를 불러옵니다.
from pathlib import Path
# 화면 없이 그림을 파일로 저장하기 위한 matplotlib 백엔드를 지정합니다.
import matplotlib
# 비대화형 백엔드를 사용합니다.
matplotlib.use("Agg")
# 막대그래프를 그리기 위해 pyplot을 불러옵니다.
import matplotlib.pyplot as plt

# 스크립트 위치를 기준으로 clean.csv 경로를 지정합니다.
CLEAN_PATH = Path(__file__).resolve().parent.parent / "data" / "clean.csv"
# 기존 그림과 별도의 범주별 그림 경로를 지정합니다.
CHART_PATH = Path(__file__).resolve().parent.parent / "charts" / "by_category.png"
# 정제 CSV만 읽습니다.
clean = pd.read_csv(CLEAN_PATH, encoding="utf-8-sig")
# 실제 범주 열과 숫자 열을 지정합니다.
CATEGORY_COLUMN = "country"
# 실제 숫자 열인 visitors를 지정합니다.
NUMBER_COLUMN = "visitors"
# 범주별 개수·합·평균을 계산하고 범주 이름순으로 정렬합니다.
summary = clean.groupby(CATEGORY_COLUMN, sort=True)[NUMBER_COLUMN].agg(["count", "sum", "mean"]).reset_index()
# 범주 이름을 문자열로 바꿉니다.
summary[CATEGORY_COLUMN] = summary[CATEGORY_COLUMN].astype(str)
# 막대 위치와 평균값을 준비합니다.
positions = range(len(summary))
# 그림 크기를 범주 수에 맞춰 지정합니다.
fig, ax = plt.subplots(figsize=(14, 7))
# 범주별 평균 막대를 그립니다.
bars = ax.bar(positions, summary["mean"])
# 각 막대 위에 평균과 n을 표시합니다.
for position, bar, mean, count in zip(positions, bars, summary["mean"], summary["count"]):
    # 평균과 표본 수를 두 줄로 표시합니다.
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f"{mean:,.0f}\nn={int(count)}", ha="center", va="bottom", fontsize=8)
# 가로축 눈금에 범주 이름을 표시합니다.
ax.set_xticks(list(positions))
# 범주 이름이 겹치지 않도록 회전합니다.
ax.set_xticklabels(summary[CATEGORY_COLUMN], rotation=45, ha="right")
# 가로축 이름을 영어로 지정합니다.
ax.set_xlabel("Country category")
# 세로축 이름을 영어로 지정합니다.
ax.set_ylabel("Average visitors (people)")
# 제목에 전체 정제 행 수를 넣습니다.
ax.set_title(f"Average visitors by country category, n = {len(clean)}")
# 막대 위 글자가 잘리지 않도록 위쪽 여백을 확보합니다.
ax.margins(y=0.15)
# 그림 여백을 자동으로 정리합니다.
fig.tight_layout()
# 그림을 파일로 저장합니다.
fig.savefig(CHART_PATH, dpi=150)
# 그림 창은 띄우지 않습니다.
plt.close(fig)
# 그룹별 표를 출력합니다.
print("| 범주 | 개수 | 합 | 평균 |\n|---|---:|---:|---:|")
# 각 그룹의 실제 통계를 출력합니다.
for _, row in summary.iterrows():
    # 평균은 소수 둘째 자리까지 표시합니다.
    print(f"| {row[CATEGORY_COLUMN]} | {int(row['count'])} | {int(row['sum'])} | {row['mean']:.2f} |")
# 그룹별 개수 합과 전체 행 수가 같은지 출력합니다.
count_sum = int(summary["count"].sum())
# 개수 합 검산 결과를 출력합니다.
print(f"개수 합: {count_sum} · 정제 행 수: {len(clean)} · {'같음' if count_sum == len(clean) else '다름'}")
