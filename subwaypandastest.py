import tkinter as tk
import pandas as pd
import numpy as np

# 엑셀 파일 불러오기
file_path = 'C:\\Users\\2C000013\\Desktop\\지하철노선.xlsx'
subway_data = pd.read_excel(file_path, sheet_name=None)

# 1호선과 2호선 데이터 불러오기
line1_data = subway_data['1호선']
line2_data = subway_data['2호선']

# 메인 윈도우 생성
root = tk.Tk()
root.title("수도권 지하철 노선도")
root.geometry("1200x900")

# 캔버스 생성
canvas = tk.Canvas(root, width=1200, height=900, bg="white")
canvas.pack()

# 역과 역 사이 연결선 그리기 함수
def draw_line(line_data, color):
    for i in range(len(line_data) - 1):
        x1, y1 = line_data.iloc[i, 1], line_data.iloc[i, 2]
        x2, y2 = line_data.iloc[i+1, 1], line_data.iloc[i+1, 2]
        canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

# 역을 그리는 함수
def draw_station(name, x, y):
    canvas.create_oval(x-7, y-7, x+7, y+7, fill="white")
    canvas.create_text(x, y+20, text=name, font=("Arial", 10))

# 1호선과 2호선의 역과 연결선 그리기
draw_line(line1_data, "blue")  # 1호선 파란색
draw_line(line2_data, "green")  # 2호선 초록색

print(line1_data.iterrows())

# 1호선의 역 표시
for i, row in line1_data.iterrows():
    #print(line1_data.at[i,"역이름"])
    name, x, y = row[0], row[1], row[2]
    draw_station(name, x, y)

# 2호선의 역 표시
for i, row in line2_data.iterrows():
    name, x, y = row[0], row[1], row[2]
    draw_station(name, x, y)

# 메인 루프 시작
root.mainloop()
