import tkinter as tk
import pandas as pd
from PIL import Image, ImageTk
import copy

# 엑셀 파일 불러오기5
#file_path = 'C:\\Users\\2C000013\\Desktop\\지하철노선.xlsx'
file_path = 'C:\\Users\\2C000013\\Downloads\\Subway_Tk-main\\수도권지하철노선 데이터 추가.xlsx'
subway_data = pd.read_excel(file_path, sheet_name=None)

# 1호선과 2호선 데이터 불러오기
line1_data = subway_data['1호선']
line2_data = subway_data['2호선']
line3_data = subway_data['3호선']
line4_data = subway_data['4호선']
line5_data = subway_data['5호선']
line6_data = subway_data['6호선']
line7_data = subway_data['7호선']
line8_data = subway_data['8호선']
line9_data = subway_data['9호선']
airport_data = subway_data['공항철도']
gyeongui_jungang_data = subway_data['경의중앙선']
gyeongchun_data = subway_data['경춘선']
suin_bundang_data = subway_data['수인분당선']
shinbundang_data = subway_data['신분당선']
gyeonggang_data = subway_data['경강선']
seohae_data = subway_data['서해선']
incheon1_data = subway_data['인천1호선']
incheon2_data = subway_data['인천2호선']
uijeongbu_data = subway_data['의정부경전철']
uisinseol_data = subway_data['우이신설선']
everline_data = subway_data['에버라인']
sinlim_data = subway_data['신림선']
gtx_a_data = subway_data['GTX-A']
uisinseol_data = subway_data['우이신설선']
gimpo_gold_data = subway_data['김포골드라인']

# 메인 윈도우 생성
root = tk.Tk()
root.title("수도권 지하철 노선도")
root.geometry("1700x1100")
root.resizable(False,False)

# 좌측(지하철 노선도)과 우측(출발역, 도착역 설정)을 나누는 프레임
left_frame = tk.Frame(root, width=1300, height=1100)
right_frame = tk.Frame(root, width=400, height=1100)


left_frame.grid(row=0, column=0, padx=0, pady=0,sticky='nsew')
right_frame.grid(row=0, column=1, padx=0, pady=0,sticky='nsew')

#image = Image.open("C:\\Users\\2C000013\\Desktop\\서울최종.png")
image = Image.open('C:\\Users\\2C000013\\Downloads\\Subway_Tk-main\\사진\\수도권지하철.png')
image_width = 1300
image_height = 1100 
margin_x = 0
margin_y = 0

resized_image = image.resize((image_width,image_height))
photo = ImageTk.PhotoImage(resized_image) 

# 캔버스 생성 (왼쪽 프레임에 위치)
canvas = tk.Canvas(left_frame, width=1300, height=1100, bg="white")

canvas.pack()

canvas.create_image(margin_x,margin_y,image=photo,anchor=tk.NW)

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
    canvas.create_oval(x-4, y-4, x+4, y+4, fill="white")
    canvas.create_text(x, y+15, text=name, font=("맑은 고딕", 9))
    
def draw_transfer_station(name,x,y):
    canvas.create_oval(x-7, y-7, x+7, y+7, fill="white")
    #canvas.create_text(x, y+20, text=name, font=("맑은 고딕", 10))

# 역을 클릭하면 출력하는 함수
def on_station_click(event):
    x, y = event.x, event.y
    for station in stations:
        station_x, station_y = station['x'], station['y']
        if abs(x - station_x) < 10 and abs(y - station_y) < 10:  # 좌표 근처 클릭 감지
            if current_textbox == 'start':
                start_station_var.set(station['name'])  # 출발역 설정
            elif current_textbox == 'end':
                end_station_var.set(station['name'])  # 도착역 설정
            print(f"{station['name']} 역이 클릭되었습니다.")
            break

# 클릭된 텍스트 박스를 기록할 변수
current_textbox = None

# 텍스트 박스 클릭 시 클릭된 텍스트 박스를 기록하는 함수
def on_textbox_click(name):
    global current_textbox
    current_textbox = name
    print(f"{name} 텍스트 박스 클릭됨")

    
# 중복 여부를 확인하는 함수
def is_station_duplicate(name, stations):
    for station in stations:
        if station['name'] == name:
            return True
    return False

# 각 호선의 데이터를 처리하기 위한 리스트
lines_data = [
    (line1_data, "#004CA1", "1호선"),           # 1호선
    (line2_data, "#1A9F58", "2호선"),          # 2호선
    (line3_data, "#EB6E1C", "3호선"),         # 3호선
    (line4_data, "#09A1D3", "4호선"),        # 4호선
    (line5_data, "#9669B3","5호선"),         # 5호선
    (line6_data, "#C08743","6호선"),          # 6호선
    (line7_data, "#65700B","7호선"),    # 7호선
    (line8_data, "#DD709C","8호선"),           # 8호선
    (line9_data, "#C0B6AD","9호선"),           # 9호선
    (airport_data, "#6AB0C1","공항철도"),       # 공항철도
    (gyeongui_jungang_data, "#6CB995","경의중앙선"), # 경의중앙선
    (gyeongchun_data, "#2E927C","경춘선"),  # 경춘선
    (suin_bundang_data, "#F6CC32","수인분당선"),   # 수인분당선
    (shinbundang_data, "#B81B4A","신분당선"),      # 신분당선
    (gyeonggang_data, "#0070C0","경강선"),  # 경강선
    (seohae_data, "#8DBF3A","서해선"),      # 서해선
    (incheon1_data, "#BFD1DF","인천1호선"),        # 인천1호선
    (incheon2_data, "#E9B867","인천2호선"),  # 인천2호선
    (uijeongbu_data, "#E4B000","의정부 경전철"),        # 의정부 경전철
    (uisinseol_data, "#CED069","우이신설선"),    # 우이신설선
    (everline_data, "#63A146","에버라인(용인경전철)"),  # 에버라인
    (sinlim_data, "#6B7D9C","신림선"),      # 신림선
    (gtx_a_data, "#905783","GTX-A"),        # GTX-A
    (gimpo_gold_data, "#C2A956","김포골드라인")        # 김포골드라인
]
    
stations = []
line_info = {}
landscape = {}

# 1호선과 2호선의 역과 연결선 그리기
for line_data, color, info in lines_data:
    # 연결선 그리기
    draw_line(line_data, color)
        
    
    # 역 그리기
    for i, row in line_data.iterrows():
        
        if pd.notna(line_data.iloc[i,0]):
            name, x, y = row.iloc[0], row.iloc[1], row.iloc[2]

            #line_info에 역 호선 정보 추가
            if name not in line_info:
                line_info[name] = []
                line_info[name].append(info)
            else :
                line_info[name].append(info)
            # landscape에 현재 역 추가
            if name not in landscape:
                landscape[name] = [] 

            # 다음 역 추가 (마지막 역이 아닌 경우)
            if i < len(line_data) - 1:
                next_station = line_data.iloc[i + 1, 0]
                if pd.notna(line_data.iloc[i+1,0]):
                    if next_station not in landscape:
                        landscape[next_station] = []
                    landscape[name].append(next_station)  # 현재 역에 다음 역 추가
                    landscape[next_station].append(name)  # 다음 역에 현재 역 추가
            
            # D열 이후의 데이터가 있는지 확인하여 landscape에 추가
            for j in range(3, len(line_data.columns)):  # 3열 이후부터(즉, D열) 확인
                connected_station_name = line_data.iloc[i, j]
                if pd.notna(connected_station_name):  # 데이터가 존재하면
                    # 연결된 역의 좌표 가져오기
                    connected_station = line_data[line_data.iloc[:, 0] == connected_station_name]
                    if not connected_station.empty:
                        landscape[name].append(connected_station.iloc[0, 0])
                        landscape[connected_station.iloc[0, 0]].append(name)


            # 역 중복 여부 확인 후 그리기
            if is_station_duplicate(name, stations):
                for station in stations:
                    if station['name'] == name:
                        draw_transfer_station(name, station['x'], station['y'])
            else:
                draw_station(name, x, y)
                stations.append({"name": name, "x": x, "y": y})

    # 역 이름에 클릭 이벤트 바인딩
    canvas.bind('<Button-1>', on_station_click)
    
#print(landscape)  # 디버그 출력
print()
print()
#print(line_info)

# ---------- 오른쪽 프레임(출발역, 도착역 설정) ----------
# 출발역, 도착역을 설정하는 콤보박스와 버튼 추가
from tkinter import ttk

station_names = sorted([station['name'] for station in stations])
# 자동완성 기능 추가를 위한 함수
def update_combobox(event, combobox, station_list):
    typed_text = combobox.get()  # 입력된 텍스트 가져오기
    if typed_text == '':
        combobox['values'] = station_list  # 아무 입력이 없으면 전체 리스트
    else:
        # 입력된 텍스트로 시작하는 역들 필터링
        filtered_stations = [station for station in station_list if station.lower().startswith(typed_text.lower())]
        combobox['values'] = filtered_stations  # 필터링된 리스트 적용
    combobox.event_generate('<Down>')  # 첫 번째 항목을 자동으로 선택되도록 설정

# 출발역 라벨과 콤보박스
start_label = tk.Label(right_frame, text="출발역 선택", font=("맑은 고딕", 12))
start_label.pack(padx = 100)

start_station_var = tk.StringVar()
start_station_combobox = ttk.Combobox(right_frame, textvariable=start_station_var, state="normal")
start_station_combobox['values'] = station_names  # 모든 역 이름 리스트로 설정
start_station_combobox.pack(pady = 20)

# 출발역 검색 시 자동완성 기능 추가
start_station_combobox.bind('<KeyRelease>', lambda event: update_combobox(event, start_station_combobox, station_names))


# 도착역 라벨과 콤보박스
end_label = tk.Label(right_frame, text="도착역 선택", font=("맑은 고딕", 12))
end_label.pack(pady=20)

end_station_var = tk.StringVar()
end_station_combobox = ttk.Combobox(right_frame, textvariable=end_station_var, state="normal")
end_station_combobox['values'] = station_names  # 모든 역 이름 리스트로 설정
end_station_combobox.pack(pady=10)

# 도착역 검색 시 자동완성 기능 추가
end_station_combobox.bind('<KeyRelease>', lambda event: update_combobox(event, end_station_combobox, station_names))

# 출발역 텍스트 박스 클릭 시
start_station_combobox.bind('<Button-1>', lambda event: on_textbox_click('start'))

# 도착역 텍스트 박스 클릭 시
end_station_combobox.bind('<Button-1>', lambda event: on_textbox_click('end'))

    
# 최단 시간 계산 함수 
def calculate_shortest_time():
    start_station = start_station_var.get()  # 출발역
    end_station = end_station_var.get()  # 도착역

    if start_station and end_station:
        print(f"출발역: {start_station}, 도착역: {end_station}")

        # 각 역에 대한 초기 설정
        routing = {}
        for place in landscape.keys():
            routing[place] = {'shortestDist': float('inf'), 'route': [], 'visited': False}

        # 출발점 초기화
        routing[start_station]['shortestDist'] = 0
        routing[start_station]['route'] = [start_station]

        # 방문할 역 처리 함수
        def visitPlace(visit, previous_line=None):
            routing[visit]['visited'] = True
            current_line = line_info[visit]  # 현재 역의 노선

            # 이전 역이 없을 경우 (즉, 출발역인 경우)
            if previous_line is None:
                previous_line = current_line

            # 현재 역에서 갈 수 있는 모든 역을 탐색
            for next_station in landscape[visit]:
                next_line = line_info[next_station]  # 다음 역의 노선

                # 환승 시간 고려: 다른 노선으로 갈아탈 경우 6분 추가
                if not set(previous_line).intersection(set(next_line)):  # 이전 역과 겹치는 노선이 없는 경우
                    additional_time = 16  # 환승 시 6분 추가
                else:
                    additional_time = 2  # 같은 노선일 경우 이동 시간은 2분

                toDist = routing[visit]['shortestDist'] + additional_time

                # 현재 기록된 거리보다 새로운 거리가 더 짧으면 업데이트
                if routing[next_station]['shortestDist'] > toDist:
                    routing[next_station]['shortestDist'] = toDist
                    routing[next_station]['route'] = copy.deepcopy(routing[visit]['route'])
                    routing[next_station]['route'].append(next_station)

            # 다음 역을 방문할 때 현재 역의 노선 정보를 전달
            for next_station in landscape[visit]:
                if not routing[next_station]['visited']:
                    visitPlace(next_station, current_line)  # current_line을 previous_line으로 전달

        # 출발점에서 첫 방문 처리
        visitPlace(start_station)

        # 다익스트라 알고리즘 실행
        while True:
            minDist = float('inf')
            toVisit = ''
            # 방문하지 않은 곳 중에서 가장 짧은 거리를 가진 역 선택
            for name, search in routing.items():
                if search['shortestDist'] < minDist and not search['visited']:
                    minDist = search['shortestDist']
                    toVisit = name
            if toVisit == '':
                break
            # 선택된 역 방문
            visitPlace(toVisit)

        # 결과 출력
        route = routing[end_station]['route']
        shortest_time = routing[end_station]['shortestDist']

        # 환승역 확인 및 각 구간 시간 계산
        transfer_stations = []
        section_times = []
        total_time = 0

        for i in range(1, len(route)):
            previous_station = route[i - 1]
            current_station = route[i]
            previous_line = line_info[previous_station]  # 이전 역의 노선 정보
            current_line = line_info[current_station]
            
            # 이전 역과 현재 역이 같은 노선이면 2분, 다른 노선이면 6분 추가
            if set(previous_line).intersection(set(current_line)):
                section_time = 2
            else:
                section_time = 16  # 환승 시 16분
            
            section_times.append(section_time)  # 구간별 소요 시간 추가
            total_time += section_time

            # 다음 역이 존재하는지 검사
            if i < len(route) - 1:  # 마지막 역이 아니면 다음 역을 검사
                next_line = line_info[route[i + 1]]  # 다음 역의 노선 정보
                
                if not set(previous_line).intersection(set(next_line)):  # 다른 노선으로 갈아탈 때
                    transfer_stations.append(current_station)  # 환승역 추가

        # 환승역과 각 구간의 소요 시간 출력
        detailed_route = []
        sum = 0
        
        for i in range(len(route) - 1):
            sum += section_times[i]
            # route[i]가 환승역에 포함되어 있는지 확인
            if route[i] in transfer_stations:
                detailed_route.append(f"{route[i]} -> {route[i + 1]} ({sum}분)")
                sum=0
        
        # 마지막 역까지 누적된 시간 출력
        detailed_route.append(f"{route[-2]} -> {route[-1]} ({sum}분)")
        
        # 환승역이 없는 경우 출력
        if not transfer_stations:
            print(f"출발역: {start_station} -> 도착역: {end_station}")
            print(f"소요 시간: {shortest_time}분")
            result_label.config(text=f"출발역: {start_station} -> 도착역: {end_station}\n소요 시간: {shortest_time}분")
        # 환승역이 있는 경우 출력
        else:
            print(f"출발역: {start_station} -> 환승역: {', '.join(transfer_stations)} -> 도착역: {end_station}")
            print(f"소요 시간: {shortest_time}분")
            print("구간별 소요 시간:")
            for section in detailed_route:
                print(section)
            result_label.config(text=f"출발역: {start_station} \n 환승역: {'\n->'.join(transfer_stations)} \n 도착역: {end_station}\n소요 시간: {shortest_time}분\n\n구간별 소요 시간:\n" + "\n".join(detailed_route))

            
# 최단 시간 계산 버튼
calculate_button = tk.Button(right_frame, text="최단 시간 계산", command=calculate_shortest_time)
calculate_button.pack(pady=30)

# 결과를 출력할 라벨
result_label = tk.Label(right_frame, text="", font=("맑은 고딕", 12))
result_label.pack(pady=20)

# 메인 루프 시작
root.mainloop()
