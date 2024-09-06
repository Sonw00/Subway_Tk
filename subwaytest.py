import tkinter as tk
import pandas as pd

# 엑셀 파일 불러오기
file_path = 'C:\\Users\\2C000013\\Desktop\\지하철노선.xlsx'
subway_data = pd.read_excel(file_path, sheet_name=None)

# 1호선과 2호선 데이터 불러오기
line1_data = subway_data['1호선'] 
line2_data = subway_data['2호선']                                      # 호선 추가

# 메인 윈도우 생성
root = tk.Tk()
root.title("수도권 지하철 노선도")
root.geometry("1200x1000")

# 캔버스 생성
canvas = tk.Canvas(root, width=1200, height=1000, bg="white")
canvas.pack()

# 역과 역 사이 연결선 그리기 함수
def draw_line(line_data, color):
    for i in range(len(line_data) - 1):
        x1, y1 = line_data.iloc[i, 1], line_data.iloc[i, 2]
        x2, y2 = line_data.iloc[i+1, 1], line_data.iloc[i+1, 2]
        canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

# 역을 그리는 함수
def draw_station(name, x, y):
    canvas.create_oval(x-5, y-5, x+5, y+5, fill="white")
    canvas.create_text(x, y+20, text=name, font=("맑은 고딕", 10))

    
def on_station_click(event, stations):
    x, y = event.x, event.y
    for station in stations:
        station_x, station_y = station['x'], station['y']
        if abs(x - station_x) < 10 and abs(y - station_y) < 10:  # 좌표 근처 클릭 감지
            print(f"{station['name']} 역이 클릭되었습니다.")
            break
    
def on_canvas_click(event):
    x, y = event.x, event.y
    print(f"Clicked at ({x}, {y})")

# 각 호선의 데이터를 처리하기 위한 리스트
lines_data = [(line1_data, "blue"), (line2_data, "green")]            # 호선 변수와 색깔 추가

stations = [
]

# 1호선과 2호선의 역과 연결선 그리기
for line_data, color in lines_data:
    # 연결선 그리기
    draw_line(line_data, color)
    
    # 역 그리기
    for i, row in line_data.iterrows():
        name, x, y = row[0], row[1], row[2]
        draw_station(name, x, y)
        stations.append({"name": name, "x": x, "y": y})
        # 역 이름에 클릭 이벤트 바인딩
        canvas.bind('<Button-1>', lambda e: on_station_click(e, stations))

# 메인 루프 시작
root.mainloop()
