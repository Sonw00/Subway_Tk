import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pandas as pd
import heapq

# 엑셀 파일 불러오기
file_path = 'C:\\py\\다익스트라\\수도권지하철노선.xlsx'
subway_data = pd.read_excel(file_path, sheet_name=None)

# 1호선, 2호선, 3호선, 4호선 데이터 불러오기
line_data = {
    '1호선': subway_data['1호선'],
    '2호선': subway_data['2호선'],
    '3호선': subway_data['3호선'],
    '4호선': subway_data['4호선']
}

# 메인 윈도우 생성
root = tk.Tk()
root.title("수도권 지하철 노선도")
root.resizable(False, False)

# 좌측(지하철 노선도)과 우측(출발역, 도착역 설정)을 나누는 프레임
left_frame = tk.Frame(root, width=1300, height=1100)
right_frame = tk.Frame(root, width=400, height=1100)

left_frame.grid(row=0, column=0, padx=0, pady=0, sticky='nsew')
right_frame.grid(row=0, column=1, padx=0, pady=0, sticky='nsew')

# 이미지 로드
image = Image.open('C:\\py\\다익스트라\\서울최종.png')
resized_image = image.resize((1500, 1000))
photo = ImageTk.PhotoImage(resized_image)

# 캔버스 생성 (왼쪽 프레임에 위치)
canvas = tk.Canvas(left_frame, width=1600, height=1100, bg="white")
canvas.pack()
canvas.create_image(80, 50, image=photo, anchor=tk.NW)

# 색상 저장을 위한 전역 변수
line_colors = {
    "1호선": "blue",
    "2호선": "green",
    "3호선": "orange",
    "4호선": "skyblue"
}

# 각 호선의 선 ID를 저장하는 딕셔너리
line_ids = {}
line_ids_original_colors = {}

# 선택된 선을 관리하는 리스트
selected_lines = []

def draw_line(line_data, color, line_name):
    line_ids[line_name] = []
    line_ids_original_colors[line_name] = color
    for i in range(len(line_data) - 1):
        if pd.notna(line_data.iloc[i, 0]) and pd.notna(line_data.iloc[i + 1, 0]):
            x1, y1 = line_data.iloc[i, 1], line_data.iloc[i, 2]
            x2, y2 = line_data.iloc[i + 1, 1], line_data.iloc[i + 1, 2]
            line_id = canvas.create_line(x1, y1, x2, y2, fill=color, width=4, tags=line_name)
            line_ids[line_name].append(line_id)

        for j in range(3, len(line_data.columns)):
            connected_station_name = line_data.iloc[i, j]
            if pd.notna(connected_station_name):
                connected_station = line_data[line_data.iloc[:, 0] == connected_station_name]
                if not connected_station.empty:
                    x_conn, y_conn = connected_station.iloc[0, 1], connected_station.iloc[0, 2]
                    line_id = canvas.create_line(x1, y1, x_conn, y_conn, fill=color, width=4, tags=line_name)
                    line_ids[line_name].append(line_id)

def on_line_click(event):
    x, y = event.x, event.y
    line_clicked = None

    for line_name in line_ids:
        for line_id in line_ids[line_name]:
            coords = canvas.coords(line_id)
            if coords and (min(coords[0], coords[2]) <= x <= max(coords[0], coords[2]) and
                           min(coords[1], coords[3]) <= y <= max(coords[1], coords[3])):
                line_clicked = line_name
                break
        if line_clicked:
            break

    if line_clicked:
        toggle_line_selection(line_clicked)
    else:
        reset_line_colors()  # 빈 공간 클릭 시 색상 복원

def toggle_line_selection(selected_line):
    if selected_line in selected_lines:
        selected_lines.remove(selected_line)
    else:
        selected_lines.append(selected_line)
    update_line_colors()

def update_line_colors():
    for line_name in line_colors:
        color = "gainsboro" if line_name not in selected_lines else line_colors[line_name]
        for line_id in line_ids[line_name]:
            canvas.itemconfig(line_id, fill=color)

def reset_line_colors():
    for line_name in line_ids:
        for line_id in line_ids[line_name]:
            canvas.itemconfig(line_id, fill=line_ids_original_colors[line_name])

def draw_station(name, x, y):
    canvas.create_oval(x - 4, y - 4, x + 4, y + 4, fill="white")
    canvas.create_text(x, y + 15, text=name, font=("맑은 고딕", 9))

def draw_transfer_station(name, x, y):
    canvas.create_oval(x - 7, y - 7, x + 7, y + 7, fill="white")

def is_station_duplicate(name, stations):
    return any(station['name'] == name for station in stations)

lines_data = [(data, line_colors[line], line) for line, data in line_data.items()]

stations = []
line_info = {}
landscape = {}

for line_data, color, info in lines_data:
    draw_line(line_data, color, info)
    
    for i, row in line_data.iterrows():
        if pd.notna(line_data.iloc[i, 0]):
            name, x, y = row.iloc[0], row.iloc[1], row.iloc[2]

            if name not in line_info:
                line_info[name] = []
            line_info[name].append(info)
                
            if name not in landscape:
                landscape[name] = []

            if i < len(line_data) - 1:
                next_station = line_data.iloc[i + 1, 0]
                if pd.notna(next_station):
                    landscape[name].append(next_station)
                    landscape[next_station] = landscape.get(next_station, []) + [name]

            for j in range(3, len(line_data.columns)):
                connected_station_name = line_data.iloc[i, j]
                if pd.notna(connected_station_name):
                    connected_station = line_data[line_data.iloc[:, 0] == connected_station_name]
                    if not connected_station.empty:
                        landscape[name].append(connected_station.iloc[0, 0])
                        landscape[connected_station.iloc[0, 0]] = landscape.get(connected_station.iloc[0, 0], []) + [name]

            if is_station_duplicate(name, stations):
                for station in stations:
                    if station['name'] == name:
                        draw_transfer_station(name, station['x'], station['y'])
            else:
                draw_station(name, x, y)
                stations.append({"name": name, "x": x, "y": y})

# 역 클릭 이벤트 바인딩
canvas.bind('<Button-1>', on_line_click)

# 오른쪽 프레임(출발역, 도착역 설정)
station_names = sorted([station['name'] for station in stations])

def update_combobox(event, combobox, station_list):
    typed_text = combobox.get()
    if typed_text == '':
        combobox['values'] = station_list
    else:
        filtered_stations = [station for station in station_list if station.startswith(typed_text)]
        combobox['values'] = filtered_stations
    combobox.event_generate('<Down>')

# 출발역 라벨과 콤보박스
start_label = tk.Label(right_frame, text="출발역 선택", font=("맑은 고딕", 12))
start_label.pack(padx=100)

start_station_var = tk.StringVar()
start_station_combobox = ttk.Combobox(right_frame, textvariable=start_station_var, state="normal")
start_station_combobox['values'] = station_names
start_station_combobox.pack(pady=20)
start_station_combobox.bind('<KeyRelease>', lambda event: update_combobox(event, start_station_combobox, station_names))

# 도착역 라벨과 콤보박스
end_label = tk.Label(right_frame, text="도착역 선택", font=("맑은 고딕", 12))
end_label.pack(padx=100)

end_station_var = tk.StringVar()
end_station_combobox = ttk.Combobox(right_frame, textvariable=end_station_var, state="normal")
end_station_combobox['values'] = station_names
end_station_combobox.pack(pady=20)
end_station_combobox.bind('<KeyRelease>', lambda event: update_combobox(event, end_station_combobox, station_names))

# 최단 시간 계산 함수
def calculate_shortest_time():
    start_station = start_station_var.get()
    end_station = end_station_var.get()

    if start_station not in landscape or end_station not in landscape:
        result_label.config(text="잘못된 역입니다.")
        return

    def dijkstra(start, end):
        distances = {station: float('inf') for station in line_info}
        distances[start] = 0
        priority_queue = [(0, start)]
        while priority_queue:
            current_distance, current_station = heapq.heappop(priority_queue)
            if current_station == end:
                return current_distance
            if current_distance > distances[current_station]:
                continue
            for neighbor in landscape.get(current_station, []):
                distance = 1
                new_distance = current_distance + distance
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    heapq.heappush(priority_queue, (new_distance, neighbor))
        return float('inf')

    shortest_time = dijkstra(start_station, end_station)
    if shortest_time == float('inf'):
        result_label.config(text="경로를 찾을 수 없습니다.")
    else:
        result_label.config(text=f"최단 시간: {shortest_time} 분")

# 계산 버튼과 결과 라벨
calculate_button = tk.Button(right_frame, text="최단 시간 계산", command=calculate_shortest_time)
calculate_button.pack(pady=20)

result_label = tk.Label(right_frame, text="", font=("맑은 고딕", 12))
result_label.pack(pady=10)

# Tkinter 메인 루프 실행
root.mainloop()
