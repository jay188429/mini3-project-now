# pandas를 불러옵니다.
import pandas as pd

# 가짜 미술관 이름과 숫자로 된 방문객수를 표로 만듭니다.
museum_data = {
    "미술관명": ["구름빵미술관", "별나라미술관", "토끼풀미술관"],
    "방문객수": [120, 85, 143],
}

# 딕셔너리로부터 pandas 표를 만듭니다.
museum_table = pd.DataFrame(museum_data)

# 표 위에 환경 확인 문구를 출력합니다.
print("환경 확인용 가상 예시")
# 표를 출력합니다.
print(museum_table)
# 표의 행과 열 개수를 출력합니다.
print(museum_table.shape)
