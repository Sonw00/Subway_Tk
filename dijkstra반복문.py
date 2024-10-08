import tkinter as tk
import pandas as pd
from PIL import Image, ImageTk
import copy

# 엑셀 파일 불러오기5
file_path = 'C:\\Users\\thsdn\\Downloads\\Subway_Tk-main\\수도권지하철노선 데이터 추가.xlsx'
#file_path = 'C:\\Users\\2C000013\\Downloads\\Subway_Tk-main\\수도권지하철노선 데이터 추가.xlsx'
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

image = Image.open("C:\\Users\\thsdn\\Downloads\\Subway_Tk-main\\사진\\수도권지하철.png")
#image = Image.open('C:\\Users\\2C000013\\Downloads\\Subway_Tk-main\\사진\\수도권지하철.png')
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
    #canvas.create_oval(x-4, y-4, x+4, y+4, fill="white")
    canvas.create_text(x, y+15, text='', font=("맑은 고딕", 9))
    
def draw_transfer_station(name,x,y):
    #canvas.create_oval(x-7, y-7, x+7, y+7, fill="white")
    canvas.create_text(x, y+20, text='', font=("맑은 고딕", 10))

            
selected_arcs = {'start': None, 'end': None}  # 출발과 도착 역 정보를 저장하는 딕셔너리
hovered_item = {'x': None, 'oval': None}  # 현재 마우스가 올려진 도형 정보

def on_station_click(event):
    global selected_arcs
    x, y = event.x, event.y
    # 출발 arc에 대한 클릭 처리
    if selected_arcs['start']:
        start_coords = canvas.coords(selected_arcs['start']['circle'])
        print("x :",x,", y:",y)
        print("start_coords:",start_coords[0],start_coords[1],start_coords[2],start_coords[3])
        if start_coords[0] <= x <= start_coords[2] and start_coords[1] <= y <= start_coords[3]:
            canvas.delete(selected_arcs['start']['arc'])
            canvas.delete(selected_arcs['start']['text'])
            canvas.delete(selected_arcs['start']['circle'])
            start_station_var.set('')  # 출발역 설정
            selected_arcs['start'] = None
            clear_hover(event)
            return "break"  # 이벤트 전파 중단

    # 도착 arc에 대한 클릭 처리
    if selected_arcs['end']:
        end_coords = canvas.coords(selected_arcs['end']['circle'])
        if end_coords[0] <= x <= end_coords[2] and end_coords[1] <= y <= end_coords[3]:
            canvas.delete(selected_arcs['end']['arc'])
            canvas.delete(selected_arcs['end']['text'])
            canvas.delete(selected_arcs['end']['circle'])
            end_station_var.set('')  # 출발역 설정
            selected_arcs['end'] = None
            clear_hover(event)
            return "break"  # 이벤트 전파 중단"""
    for station in stations:
        station_x, station_y = station['x'], station['y']
        if abs(x - station_x) < 10 and abs(y - station_y) < 10:  # 좌표 근처 클릭 감지
            # 출발 지점 선택
            if not selected_arcs['start']:
                if selected_arcs['end'] and station['name'] == selected_arcs['end']['station']:
                    break
                arc = canvas.create_arc(station_x - 40, station_y - 40, station_x + 40, station_y + 40,
                                        start=60, extent=60, fill="red",outline=None)
                circle = canvas.create_oval(station_x-20,station_y-56,station_x+20,station_y-20,fill="red",outline=None)
                text = canvas.create_text(station_x, station_y - 38, text="출발", fill="white", font=("맑은 고딕", 9))
                selected_arcs['start'] = {'arc': arc,'circle':circle, 'text': text, 'station': station['name']}
                start_station_var.set(station['name'])  # 출발역 설정
            # 도착 지점 선택 (출발이 선택된 상태에서)
            elif not selected_arcs['end'] and station['name'] != selected_arcs['start']['station']:
                if selected_arcs['start'] and station['name'] == selected_arcs['start']['station']:
                    break
                arc = canvas.create_arc(station_x - 40, station_y - 40, station_x + 40, station_y + 40,
                                        start=60, extent=60, fill="blue",outline=None)
                circle = canvas.create_oval(station_x-20,station_y-56,station_x+20,station_y-20,fill="blue",outline=None)
                text = canvas.create_text(station_x, station_y - 38, text="도착", fill="white", font=("맑은 고딕", 9))
                selected_arcs['end'] = {'arc': arc,'circle':circle, 'text': text, 'station': station['name']}
                end_station_var.set(station['name'])  # 도착역 설정
            break
    
    canvas.bind("<Motion>", on_hover)  # 마우스가 움직일 때 hover 이벤트 활성화
    canvas.bind("<Leave>", clear_hover)  # 캔버스에서 마우스가 벗어나면 hover 초기화
    

def on_hover(event):
    global hovered_item
    x, y = event.x, event.y
    
    # 출발 arc에 마우스가 올려졌는지 확인
    if selected_arcs['start']:
        start_coords = canvas.coords(selected_arcs['start']['circle'])
        if start_coords[0] <= x <= start_coords[2] and start_coords[1] <= y <= start_coords[3]:
            if not hovered_item['x']:  # X 표시가 없으면 추가
                margin = 2
                move_x = 19
                move_y = 0
                hovered_item['oval'] = canvas.create_oval(start_coords[2]-26-margin+move_x, start_coords[1]+2-margin+move_y, 
                                                        start_coords[2]-18+margin+move_x, start_coords[1]+10+margin+move_y, 
                                                        fill="white", outline="black")

                hovered_item['x'] = canvas.create_text(start_coords[2]-22+move_x, start_coords[1]+6+move_y, 
                                                    text="X", fill="black", font=("맑은 고딕", 10))
            return
    
    # 도착 arc에 마우스가 올려졌는지 확인
    if selected_arcs['end']:
        end_coords = canvas.coords(selected_arcs['end']['circle'])
        if end_coords[0] <= x <= end_coords[2] and end_coords[1] <= y <= end_coords[3]:
            if not hovered_item['x']:  # X 표시가 없으면 추가
                margin = 2
                move_x = 19
                move_y = 0
                hovered_item['oval'] = canvas.create_oval(end_coords[2]-26-margin+move_x, end_coords[1]+2-margin+move_y, 
                                                        end_coords[2]-18+margin+move_x, end_coords[1]+10+margin+move_y, 
                                                        fill="white", outline="black")

                hovered_item['x'] = canvas.create_text(end_coords[2]-22+move_x, end_coords[1]+6+move_y, 
                                                    text="X", fill="black", font=("맑은 고딕", 10))
            return
    
    # 아무 arc에도 마우스가 없으면 X 표시 제거
    clear_hover(event)

def clear_hover(event):
    global hovered_item
    if hovered_item['x']:
        canvas.delete(hovered_item['x'])  # X 표시 제거
        hovered_item['x'] = None
    if hovered_item['oval']:
        canvas.delete(hovered_item['oval'])  # 원형 표시 제거
        hovered_item['oval'] = None



# 클릭 이벤트 연결
canvas.bind("<Button-1>", on_station_click)


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

def on_combobox_select(event,type):
    selected_value = event.widget.get()
    for station in stations:
        if station['name'] == selected_value:
            station_x, station_y = station['x'], station['y']
            if type=='start':
                print(f"출발 역 선택: {selected_value}")
                if selected_arcs['start']:
                    canvas.delete(selected_arcs['start']['arc'])
                    canvas.delete(selected_arcs['start']['text'])
                    canvas.delete(selected_arcs['start']['circle'])
                    selected_arcs['start'] = None
                arc = canvas.create_arc(station_x - 40, station_y - 40, station_x + 40, station_y + 40,
                                        start=60, extent=60, fill="red",outline=None)
                circle = canvas.create_oval(station_x-20,station_y-56,station_x+20,station_y-20,fill="red",outline=None)
                text = canvas.create_text(station_x, station_y - 38, text="출발", fill="white", font=("맑은 고딕", 9))
                selected_arcs['start'] = {'arc': arc,'circle':circle, 'text': text, 'station': station['name']}
                start_station_var.set(station['name'])  # 도착역 설정
                
            elif type=='end':
                print(f"도착 역 선택: {selected_value}")
                if selected_arcs['end']:
                    canvas.delete(selected_arcs['end']['arc'])
                    canvas.delete(selected_arcs['end']['text'])
                    canvas.delete(selected_arcs['end']['circle'])
                    selected_arcs['end'] = None
                
                arc = canvas.create_arc(station_x - 40, station_y - 40, station_x + 40, station_y + 40,
                                        start=60, extent=60, fill="blue",outline=None)
                circle = canvas.create_oval(station_x-20,station_y-56,station_x+20,station_y-20,fill="blue",outline=None)
                text = canvas.create_text(station_x, station_y - 38, text="도착", fill="white", font=("맑은 고딕", 9))
                selected_arcs['end'] = {'arc': arc,'circle':circle, 'text': text, 'station': station['name']}
                end_station_var.set(station['name'])  # 도착역 설정

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
    #draw_line(line_data, color)
        
    
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

# 콤보박스에서 항목이 선택되었을 때 실행되는 이벤트 바인딩
start_station_combobox.bind("<<ComboboxSelected>>", lambda event: on_combobox_select(event, 'start'))
end_station_combobox.bind("<<ComboboxSelected>>", lambda event: on_combobox_select(event, 'end'))

def search_stored_stations(stored_stations):    # 저장했던 검색할 역중에 하나 반환
    for station_info in stored_stations:
        print(station_info["station"],end=", ")
    print("역 중에서 ",end="")
    for stored_station in stored_stations:
        visit = stored_station["station"]
        route = stored_station["route"]
        shortestTime = stored_station["shortestTime"]
        stored_stations.remove(stored_station)
        next_stations = landscape[visit].copy()
        next_stations = list(set(next_stations) - set(route))  # 이미 방문한 역 제외
        if len(next_stations) > 0:
            print(visit+"역에서 재검색")
            
            return visit,next_station, route, shortestTime, stored_stations, next_stations
        else :
            print(visit+"역 삭제 ")
            
    if len(stored_stations) == 0:
        print("저장된 역 정보가 없습니다.")
        return None, None, None, None, [], []  # 적절한 종료 값을 반환
        
    print("모든 저장된 역 방문을 마쳤습니다.")
    return None, None, None, None, [], []  # 적절한 종료 값을 반환

    
def calculate_shortest_time():
    start_station = start_station_var.get()  # 출발역
    end_station = end_station_var.get()  # 도착역

    if start_station and end_station:
        print(f"출발역: {start_station}, 도착역: {end_station}")
        
        # 각 역에 대한 초기 설정
        route = None
        routing = []
        visited = set()  # 방문한 역 기록
        #for place in landscape.keys():
        #    routing[place] = {'shortestDist': float('inf'), 'route': [], 'toVisit': False}
            
        #print("landscape.keys:",landscape.keys())
        #for place in landscape.keys():

        # 방문할 역 처리 함수
        def visitPlace(visit, route, shortestTime):
            
            #routing[visit]['visited'] = True
            print()
            print("재귀호출된 역:",visit)
            print("현재까지 경로: ",route)
            stored_stations = []

            # 이전 역이 없을 경우 (즉, 출발역인 경우)
            if not route:
                route = []
                
            current_line = line_info[visit]  # 현재 역의 노선
            
            next_stations = landscape[visit].copy() # 이전 역을 제외하고 갈 수 있는 다음 역 리스트
            next_stations = list(set(next_stations) - set(route))
            print("next_stations:",next_stations,", route:",route)
            while True:
                if len(next_stations) == 1:
                    next_station = next_stations[0]  # next_station 할당
                    previous_station = route[-1] if route else ''
                    previous_line = line_info[previous_station] if previous_station else []
                    print(next_station,"->",end="")
                    next_line = line_info[next_station]  # 이 줄 추가
                    if not set(previous_line).intersection(set(next_line)):
                        shortestTime += 6  # 환승 시 6분 추가
                    else:
                        shortestTime += 2  # 같은 노선일 경우 2분 추가
                    route.append(visit)
                    if next_station == end_station:
                        new_route = route.copy() + [next_station]  # 마지막 역 추가
                        routing.append({"route": new_route, "shortestTime": shortestTime})
                        print("추가된 도착 경로 : ",new_route)
                        # stored_stations 의 역이름과 경로를 다음 역으로 설정
                        visit, next_station, route, shortestTime, stored_stations,next_stations = search_stored_stations(stored_stations)
                        if visit is None or len(next_stations) == 0:  # 더 이상 저장된 역이 없는 경우
                            print("경로 탐색이 완료되었습니다.")
                            return
                    visit = next_stations[0]
                    next_stations = landscape[visit].copy()  # 새로운 역의 다음 역 갱신
                    next_stations = list(set(next_stations) - set(route))  # 이미 방문한 역 제외
                elif len(next_stations)<=0:
                    # stored_stations 의 역이름과 경로를 다음 역으로 설정
                    print(visit,'역에서 검색 중지')
                    visit, next_station, route, shortestTime, stored_stations,next_stations = search_stored_stations(stored_stations)
                    if visit is None or len(next_stations) == 0:  # 더 이상 저장된 역이 없는 경우
                            print("경로 탐색이 완료되었습니다.")
                            return
                    
                
                elif len(next_stations) >= 2:       # 갈림길일 때
                    next_station = next_stations[0]
                    print(next_stations,"역 중에서",next_station,"으로 이동")
                    previous_station = route[-1] if route else ''
                    previous_line = line_info[previous_station] if previous_station else []
                    route.append(visit)
                    for stored_station in next_stations[1:]:
                        storedTime = shortestTime
                        if not set(previous_line).intersection(set(line_info[stored_station])):
                            storedTime += 6  # 환승 시 6분 추가
                        else:
                            storedTime += 2  # 같은 노선일 경우 2분 추가
                        if stored_station == end_station:
                            new_route = route.copy() + [stored_station]  # 마지막 역 추가
                            routing.append({"route": new_route, "shortestTime": storedTime})
                            print("추가된 도착 경로 : ",new_route)
                        else:
                            stored_stations.append({"station":stored_station, "route":route,"shortestTime":storedTime})
                            print(stored_station,"역 저장")
                    next_line = line_info[next_station]
                    #original_shortest_time = shortestTime
                    # 환승 시간 고려
                    if not set(previous_line).intersection(set(next_line)):
                        shortestTime += 6  # 환승 시 6분 추가
                    else:
                        shortestTime += 2  # 같은 노선일 경우 2분 추가
                    
                    if next_station == end_station:
                        new_route = route.copy() + [stored_station]  # 마지막 역 추가
                        routing.append({"route": new_route, "shortestTime": shortestTime})
                        print("추가된 도착 경로 : ",new_route)
                        #stored_stations의 역이름과 경로를 다음 역으로 설정
                        visit, next_station, route, shortestTime, stored_stations,next_stations = search_stored_stations(stored_stations)
                        if visit is None or len(next_stations) == 0:  # 더 이상 저장된 역이 없는 경우
                            print("경로 탐색이 완료되었습니다.")
                            return
                    
                    
                    visit = next_stations[0]
                    next_stations = landscape[visit].copy()  # 새로운 역의 다음 역 갱신
                    next_stations = list(set(next_stations) - set(route))  # 이미 방문한 역 제외
                    
                
                
                    

        # 출발점에서 첫 방문 처리
        visitPlace(start_station,[],0)

        # 최단 경로 및 시간 계산
        minDist = float('inf')
        shortest_route = None

        print("검색된 경로 : ",end="")
        for route_info in routing:
            print(route_info['route'])
            if route_info['shortestTime'] < minDist:
                minDist = route_info['shortestTime']
                shortest_route = route_info['route']

        # 결과 출력
        if shortest_route is None:
            print("경로를 찾지 못했습니다.")
        else:
            print(f"최단 경로: {shortest_route}, 시간: {minDist}")
            
        """
        # 환승역 확인 및 각 구간 시간 계산
        transfer_stations = []
        section_times = []
        total_time = 0
        for i in range(1, len(route)):
            previous_station = route[i - 1]
            current_station = route[i]
            previous_line = line_info[previous_station]  # 이전 역의 노선 정보
            current_line = line_info[current_station]
            
            section_time = 2

            # 다음 역이 존재하는지 검사
            if i < len(route) - 1:  # 마지막 역이 아니면 다음 역을 검사
                next_station = route[i+1]
                next_line = line_info[next_station]
                if not set(previous_line).intersection(set(next_line)):  # 다른 노선으로 갈아탈 때
                    transfer_stations.append(current_station)  # 환승역 추가
                    section_time = 6
                    
            section_times.append(section_time)  # 구간별 소요 시간 추가
            total_time += section_time

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
"""
            
# 최단 시간 계산 버튼
calculate_button = tk.Button(right_frame, text="최단 시간 계산", command=calculate_shortest_time)
calculate_button.pack(pady=30)

# 결과를 출력할 라벨
result_label = tk.Label(right_frame, text="", font=("맑은 고딕", 12))
result_label.pack(pady=20)

# 메인 루프 시작
root.mainloop()
