import tkinter as tk
import pandas as pd

# 엑셀 파일 불러오기
#file_path = 'C:\\Users\\2C000013\\Desktop\\지하철노선.xlsx'
file_path = 'C:\\Users\\thsdn\\Downloads\\Subway_Tk-main\\지하철노선.xlsx'
subway_data = pd.read_excel(file_path, sheet_name=None)

# 1호선과 2호선 데이터 불러오기
line1_data = subway_data['1호선']
line2_data = subway_data['2호선']

# 메인 윈도우 생성
root = tk.Tk()
root.title("수도권 지하철 노선도")
root.geometry("1400x900")
root.resizable(False,False)

# 좌측(지하철 노선도)과 우측(출발역, 도착역 설정)을 나누는 프레임
left_frame = tk.Frame(root, width=1000, height=900)
right_frame = tk.Frame(root, width=400, height=900)

left_frame.grid(row=0, column=0, padx=0, pady=0)
right_frame.grid(row=0, column=1, padx=0, pady=0)

# 캔버스 생성 (왼쪽 프레임에 위치)
canvas = tk.Canvas(left_frame, width=1000, height=900, bg="white")
canvas.pack()

# 역과 역 사이 연결선 그리기 함수
def draw_line(line_data, color):
    for i in range(len(line_data) - 1):
        if pd.notna(line_data.iloc[i,0]) and pd.notna(line_data.iloc[i+1,0]):
            x1, y1 = line_data.iloc[i, 1], line_data.iloc[i, 2]
            x2, y2 = line_data.iloc[i+1, 1], line_data.iloc[i+1, 2]
            canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

        # D열 이후의 데이터가 있는지 확인하여 추가 연결선 그리기
        for j in range(3, len(line_data.columns)):  # 3열 이후부터(즉, D열) 확인
            connected_station_name = line_data.iloc[i, j]
            if pd.notna(connected_station_name):  # 데이터가 존재하면
                # 연결된 역의 좌표 가져오기
                connected_station = line_data[line_data.iloc[:, 0] == connected_station_name]
                if not connected_station.empty:
                    x_conn, y_conn = connected_station.iloc[0, 1], connected_station.iloc[0, 2]
                    canvas.create_line(x1, y1, x_conn, y_conn, fill=color, width=2)


# 역을 그리는 함수
def draw_station(name, x, y):
    canvas.create_oval(x-5, y-5, x+5, y+5, fill="white")
    canvas.create_text(x, y+20, text=name, font=("맑은 고딕", 10))
    
def draw_transfer_station(name,x,y):
    canvas.create_oval(x-8, y-8, x+8, y+8, fill="white")
    canvas.create_text(x, y+20, text=name, font=("맑은 고딕", 10))

# 역을 클릭하면 출력하는 함수
def on_station_click(event, stations):
    x, y = event.x, event.y
    for station in stations:
        station_x, station_y = station['x'], station['y']
        if abs(x - station_x) < 10 and abs(y - station_y) < 10:  # 좌표 근처 클릭 감지
            print(f"{station['name']} 역이 클릭되었습니다.")
            break
    
    
# 중복 여부를 확인하는 함수
def is_station_duplicate(name, stations):
    for station in stations:
        if station['name'] == name:
            return True
    return False

# 각 호선의 데이터를 처리하기 위한 리스트
lines_data = [(line1_data, "blue"), (line2_data, "green")]

stations = []

landscape = {}

# 1호선과 2호선의 역과 연결선 그리기
for line_data, color in lines_data:
    # 연결선 그리기
    draw_line(line_data, color)
    
    # 역 그리기
    for i, row in line_data.iterrows():
        if pd.notna(line_data.iloc[i,0]):
            name, x, y = row.iloc[0], row.iloc[1], row.iloc[2]

            # landscape에 현재 역 추가
            if name not in landscape:
                landscape[name] = []

            # 다음 역 추가 (마지막 역이 아닌 경우)
            if i < len(line_data) - 1:
                next_station = line_data.iloc[i + 1, 0]
                if next_station not in landscape:
                    landscape[next_station] = []
                if pd.notna(line_data.iloc[i+1,0]):
                    landscape[name].append(next_station)  # 현재 역에 다음 역 추가
                    landscape[next_station].append(name)  # 다음 역에 현재 역 추가


            # 역 중복 여부 확인 후 그리기
            if is_station_duplicate(name, stations):
                draw_transfer_station(name, x, y)
            else:
                draw_station(name, x, y)
                stations.append({"name": name, "x": x, "y": y})

            print(name,landscape[name])  # 디버그 출력
        
        
    # 역 이름에 클릭 이벤트 바인딩
    canvas.bind('<Button-1>', lambda e: on_station_click(e, stations))
    #print(pd.notna(line_data.iloc[i+1.1]))

# ---------- 오른쪽 프레임(출발역, 도착역 설정) ----------
# 출발역, 도착역을 설정하는 콤보박스와 버튼 추가
from tkinter import ttk

# 출발역 라벨과 콤보박스
start_label = tk.Label(right_frame, text="출발역 선택", font=("맑은 고딕", 12))
start_label.pack(padx = 100)

start_station_var = tk.StringVar()
start_station_combobox = ttk.Combobox(right_frame, textvariable=start_station_var, state="readonly")
start_station_combobox['values'] = [station['name'] for station in stations]  # 모든 역 이름 리스트로 설정
start_station_combobox.pack(pady=10)

# 도착역 라벨과 콤보박스
end_label = tk.Label(right_frame, text="도착역 선택", font=("맑은 고딕", 12))
end_label.pack(pady=20)

end_station_var = tk.StringVar()
end_station_combobox = ttk.Combobox(right_frame, textvariable=end_station_var, state="readonly")
end_station_combobox['values'] = [station['name'] for station in stations]  # 모든 역 이름 리스트로 설정
end_station_combobox.pack(pady=10)

# 최단 시간 계산 함수 (임시로 출발역과 도착역만 출력)
def calculate_shortest_time():
    start_station = start_station_var.get()
    end_station = end_station_var.get()
    if start_station and end_station:
        print(f"출발역: {start_station}, 도착역: {end_station}")
        # 여기에서 실제 최단 시간을 계산하는 알고리즘을 추가
        result_label.config(text=f"출발역: {start_station}, 도착역: {end_station}\n최단 시간: (계산 중)")

# 최단 시간 계산 버튼
calculate_button = tk.Button(right_frame, text="최단 시간 계산", command=calculate_shortest_time)
calculate_button.pack(pady=30)

# 결과를 출력할 라벨
result_label = tk.Label(right_frame, text="", font=("맑은 고딕", 12))
result_label.pack(pady=20)

# 메인 루프 시작
root.mainloop()
