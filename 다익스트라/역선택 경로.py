import tkinter as tk
from PIL import Image, ImageTk
import pandas as pd

# 엑셀 파일 불러오기
file_path = 'C:\\py\\다익스트라\\지하철노선.xlsx'
subway_data = pd.read_excel(file_path, sheet_name=None)

# 각 호선 데이터 불러오기
lines_data = [
    (subway_data['1호선'], "blue", "1호선"),
    (subway_data['2호선'], "green", "2호선"),
    (subway_data['3호선'], "orange", "3호선"),
    (subway_data['4호선'], "skyblue", "4호선"),
    (subway_data['5호선'], "purple", "5호선"),
    (subway_data['6호선'], "brown", "6호선"),
    (subway_data['7호선'], "forestgreen", "7호선"),
    (subway_data['8호선'], "pink", "8호선"),
    (subway_data['9호선'], "gold", "9호선"),
]

# 메인 윈도우 생성
root = tk.Tk()
root.title("수도권 지하철 노선도")
root.resizable(False, False)

# 좌측(지하철 노선도)과 우측(출발역, 도착역 설정)을 나누는 프레임
left_frame = tk.Frame(root, width=1900, height=1100)
left_frame.grid(row=0, column=0, padx=0, pady=0, sticky='nsew')

# 이미지 불러오기
image = Image.open('C:\\py\\다익스트라\\지도찐최종.png')
image_width = 2200
image_height = 1100
resized_image = image.resize((image_width, image_height))
photo = ImageTk.PhotoImage(resized_image)

# 캔버스 생성
canvas = tk.Canvas(left_frame, width=1900, height=1100, bg="darkgray")
canvas.pack()
canvas.create_image(0, 0, image=photo, anchor=tk.NW)

# 연결선을 그리는 함수
def draw_line(line_data, color):
    for i in range(len(line_data) - 1):
        if pd.notna(line_data.iloc[i, 0]) and pd.notna(line_data.iloc[i + 1, 0]):
            x1, y1 = line_data.iloc[i, 1], line_data.iloc[i, 2]
            x2, y2 = line_data.iloc[i + 1, 1], line_data.iloc[i + 1, 2]
            canvas.create_line(x1, y1, x2, y2, fill=color, width=5, tags="line")

# 역을 그리는 함수
def draw_station(name, x, y):
    canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill="white")
    canvas.create_text(x, y + 15, text=name, font=("맑은 고딕", 9))

# 선택된 호선만 그리는 함수
def draw_selected_line(line_data, color):
    draw_line(line_data, color)

# 역 클릭 이벤트
def on_station_click(event, stations):
    x, y = event.x, event.y
    clicked_lines = set()  # 클릭된 역과 연결된 모든 호선 추적
    for station in stations:
        station_x, station_y = station['x'], station['y']
        if abs(x - station_x) < 10 and abs(y - station_y) < 10:
            clicked_lines.add(station['line'])  # 클릭된 역의 호선 추가
            print(f"{station['name']} 역이 클릭되었습니다.")
    
    # 현재 캔버스의 모든 선을 지웁니다.
    canvas.delete("line")
    # 클릭된 역과 연결된 모든 호선 그리기
    for line_data, color, info in lines_data:
        if info in clicked_lines:
            draw_selected_line(line_data, color)

# 각 호선의 역과 연결선 그리기
stations = []
for line_data, color, info in lines_data:
    for i, row in line_data.iterrows():
        if pd.notna(row[0]):
            name, x, y = row.iloc[0], row.iloc[1], row.iloc[2]
            draw_station(name, x, y)
            stations.append({"name": name, "x": x, "y": y, "line": info})

# 역 이름에 클릭 이벤트 바인딩
canvas.bind('<Button-1>', lambda e: on_station_click(e, stations))

# 메인 루프 시작
root.mainloop()
