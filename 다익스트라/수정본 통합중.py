import tkinter as tk
import pandas as pd
from PIL import Image, ImageTk
import copy

def on_image_click(event):
    image_id = event.widget.find_withtag('current')[0]
    print(f"{image_id} image clicked!")
    toggle_image(image_id)
    
    
selected_index = None  # 선택된 버튼의 인덱스 (초기에는 None)

def toggle_image(image_id):
    global image_refs, button_images, button_ids, button_states, selected_image, selected_index

    # 버튼 이미지 정보를 가져옵니다
    button_index = button_ids.index(image_id)

    
    if selected_index is not None and selected_index != button_index:
        # 이전에 선택된 버튼을 원래 이미지로 복원
        original_image = image_refs[selected_index]["original"]
        canvas.itemconfig(button_ids[selected_index], image=original_image)
        button_states[selected_index] = 'original'
        
    # 현재 상태를 확인합니다
    current_state = button_states[button_index]
    
    if current_state == 'original':
        # 새로운 이미지로 전환
        new_button_image = image_refs[button_index]["new"]
        canvas.itemconfig(image_id, image=new_button_image)
        end_station_var.set(button_images[button_index][5])  # 텍스트 설정
        button_states[button_index] = 'new'
        selected_index = button_index  # 선택된 버튼 업데이트
    else:
        # 원래 이미지로 되돌리기
        original_image = image_refs[button_index]["original"]
        canvas.itemconfig(image_id, image=original_image)
        end_station_var.set('')
        button_states[button_index] = 'original'
        selected_index = None  # 선택된 버튼 초기화
        
    

file_path = 'C:\\py\\다익스트라\\지하철노선.xlsx'
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


# 메인 윈도우 생성
root = tk.Tk()
root.title("Subway")







# Canvas 위젯 생성
canvas = tk.Canvas(root, width=1900, height=1100, background="darkgray")
canvas.pack()

left_frame = tk.Frame(root, width=400, height=400,bg='lightgray')
left_frame.place(x=0,y=0)

# 배경 이미지 로드 및 크기 조정
background_image_path = "C:\\py\\다익스트라\\지도찐최종.png"  # 이미지 파일 경로를 바꾸세요
background_image = Image.open(background_image_path)
background_image_resized = background_image.resize((2200, 1100))
background_tk_image = ImageTk.PhotoImage(background_image_resized)

# Canvas에 배경 이미지 표시
canvas.create_image(0, 0, anchor=tk.NW, image=background_tk_image)

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
    #canvas.create_oval(x-7, y-7, x+7, y+7, fill="white")
    canvas.create_oval(x-4, y-4, x+4, y+4, fill="white")
    canvas.create_text(x, y+15, text=name, font=("맑은 고딕", 9))
    #canvas.create_text(x, y+20, text=name, font=("맑은 고딕", 10))

            
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
            #end_station_var.set('')  # 출발역 설정
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
            """elif not selected_arcs['end'] and station['name'] != selected_arcs['start']['station']:
                if selected_arcs['start'] and station['name'] == selected_arcs['start']['station']:
                    break
                arc = canvas.create_arc(station_x - 40, station_y - 40, station_x + 40, station_y + 40,
                                        start=60, extent=60, fill="blue",outline=None)
                circle = canvas.create_oval(station_x-20,station_y-56,station_x+20,station_y-20,fill="blue",outline=None)
                text = canvas.create_text(station_x, station_y - 38, text="도착", fill="white", font=("맑은 고딕", 9))
                selected_arcs['end'] = {'arc': arc,'circle':circle, 'text': text, 'station': station['name']}
                #end_station_var.set(station['name'])  # 도착역 설정"""
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
    global selected_index
    selected_value = event.widget.get()
    if type=='start':
        for station in stations:
            if station['name'] == selected_value:
                station_x, station_y = station['x'], station['y']
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
        for button_index, button_image in enumerate(button_images):
            if button_image[5] == selected_value:
                print(f"도착 랜드마크 선택: {selected_value}")
                if selected_index is not None :
                    original_image = image_refs[selected_index]["original"]
                    canvas.itemconfig(button_ids[selected_index], image=original_image)
                    button_states[selected_index] = 'original'
                # 새로 선택된 버튼의 이미지 변경
                new_button_image = image_refs[button_index]["new"]
                canvas.itemconfig(button_ids[button_index], image=new_button_image)
                end_station_var.set(button_images[button_index][5])  # 텍스트 설정
                button_states[button_index] = 'new'
                selected_index = button_index  # 선택된 버튼 업데이트
                break  # 일치하는 랜드마크를 찾았으면 루프 종료

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
    (line9_data, "#C0B6AD","9호선")             # 9호선
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


# 버튼 이미지 로드 및 크기 조정
button_images = [
    ("C:\\py\\다익스트라\\흥인지문.png", 80, 35, 1270, 450, "흥인지문", 8, "C:\\py\\다익스트라\\흥인지문2.png"),
    ("C:\\py\\다익스트라\\종묘.png", 90, 30, 1200, 480, "종묘", 8, "C:\\py\\다익스트라\\종묘2.png"),    
    ("C:\\py\\다익스트라\\남산타워.png", 80, 210, 1160, 455, "남산타워", 5, "C:\\py\\다익스트라\\남산타워2.png"),
    ("C:\\py\\다익스트라\\63빌딩.png", 50, 115, 945, 585, "63빌딩", -20, "C:\\py\\다익스트라\\63빌딩2.png"),
    ("C:\\py\\다익스트라\\노량진.png", 80, 40, 970, 725, "노량진\n수산시장", 15, "C:\\py\\다익스트라\\노량진2.png"),
    ("C:\\py\\다익스트라\\현충원.png", 130, 70, 1020, 745, "국립서울현충원", 15, "C:\\py\\다익스트라\\현충원2.png"),
    ("C:\\py\\다익스트라\\예술의전당.png", 130, 50, 1170, 790, "예술의전당", 15, "C:\\py\\다익스트라\\예술의전당2.png"),
    ("C:\\py\\다익스트라\\코엑스.png", 90, 50, 1340, 770, "코엑스", 7, "C:\\py\\다익스트라\\코엑스2.png"),
    ("C:\\py\\다익스트라\\봉은사.png", 50, 70, 1360, 670, "봉은사", 7, "C:\\py\\다익스트라\\봉은사2.png"),
    ("C:\\py\\다익스트라\\서울숲.png", 70, 70, 1350, 580, "서울숲", 3, "C:\\py\\다익스트라\\서울숲2.png"),
    ("C:\\py\\다익스트라\\성수동.png", 110, 50, 1430, 590, "성수동\n카페거리", 15, "C:\\py\\다익스트라\\성수동2.png"),
    ("C:\\py\\다익스트라\\용마산.png", 100, 80, 1460, 460, "용마산", -35, "C:\\py\\다익스트라\\용마산2.png"),
    ("C:\\py\\다익스트라\\아차산.png", 90, 70, 1480, 510, "아차산", 6, "C:\\py\\다익스트라\\아차산2.png"),
    ("C:\\py\\다익스트라\\잠실종합운동장.png", 90, 60, 1440, 710, "잠실종합운동장", 7, "C:\\py\\다익스트라\\잠실종합운동장2.png"),
    ("C:\\py\\다익스트라\\선정릉.png", 60, 40, 1310, 700, "선정릉", 7, "C:\\py\\다익스트라\\선정릉2.png"),
    ("C:\\py\\다익스트라\\서울대.png", 50, 60, 980, 815, "서울대학교", 15, "C:\\py\\다익스트라\\서울대2.png"),
    ("C:\\py\\다익스트라\\DDP.png", 110, 40, 1260, 510, "DDP", 8, "C:\\py\\다익스트라\\DDP2.png"),
    ("C:\\py\\다익스트라\\명동성당.png", 60, 70, 1130, 535, "명동성당", 8, "C:\\py\\다익스트라\\명동성당2.png"),
    ("C:\\py\\다익스트라\\광화문.png", 110, 60, 1080, 460, "광화문", 8, "C:\\py\\다익스트라\\광화문2.png"),
    ("C:\\py\\다익스트라\\경복궁.png", 90, 60, 1090, 385, "경복궁", 8, "C:\\py\\다익스트라\\경복궁2.png"),
    ("C:\\py\\다익스트라\\창덕궁.png", 70, 40, 1170, 380, "창덕궁", 8, "C:\\py\\다익스트라\\창덕궁2.png"),
    ("C:\\py\\다익스트라\\창경궁.png", 70, 30, 1210, 430, "창경궁", 8, "C:\\py\\다익스트라\\창경궁2.png"),
    ("C:\\py\\다익스트라\\이태원.png", 70, 80, 1090, 620, "이태원", 8, "C:\\py\\다익스트라\\이태원2.png"),
    ("C:\\py\\다익스트라\\국회의사당.png", 70, 35, 880, 615, "국회의사당", 8, "C:\\py\\다익스트라\\국회의사당2.png"),
    ("C:\\py\\다익스트라\\시청.png", 80, 40, 1060, 530, "시청", 8, "C:\\py\\다익스트라\\시청2.png"),
    ("C:\\py\\다익스트라\\덕수궁.png", 80, 40, 990, 510, "덕수궁", 8, "C:\\py\\다익스트라\\덕수궁2.png"),
    ("C:\\py\\다익스트라\\서울역.png", 90, 40, 920, 540, "문화역서울", 8, "C:\\py\\다익스트라\\서울역2.png"),
    ("C:\\py\\다익스트라\\서울월드컵경기장.png", 100, 60, 830, 480, "서울월드컵경기장", 8, "C:\\py\\다익스트라\\서울월드컵경기장2.png"),
    ("C:\\py\\다익스트라\\월드컵공원.png", 60, 40, 770, 480, "월드컵공원", 8, "C:\\py\\다익스트라\\월드컵공원2.png"),
    ("C:\\py\\다익스트라\\김포공항.png", 100, 35, 440, 530, "김포국제공항", 8, "C:\\py\\다익스트라\\김포공항2.png"),
    ("C:\\py\\다익스트라\\서울식물원.png", 100, 50, 630, 540, "서울식물원", 8, "C:\\py\\다익스트라\\서울식물원2.png"),
    ("C:\\py\\다익스트라\\고척돔.png", 100, 50, 710, 720, "고척스카이돔", 8, "C:\\py\\다익스트라\\고척돔2.png"),
    ("C:\\py\\다익스트라\\독립문2.png", 40, 40, 970, 450, "독립문", 8, "C:\\py\\다익스트라\\독립문.png"),
    ("C:\\py\\다익스트라\\서대문형무소.png", 70, 40, 930, 390, "서대문형무소\n역사관", 15, "C:\\py\\다익스트라\\서대문형무소2.png"),
    ("C:\\py\\다익스트라\\숭례문.png", 90, 50, 1000, 570, "숭례문", 8, "C:\\py\\다익스트라\\숭례문2.png"),
    ("C:\\py\\다익스트라\\청와대.png", 110, 40, 1015, 349, "청와대", 8, "C:\\py\\다익스트라\\청와대2.png"),
    ("C:\\py\\다익스트라\\북한산.png", 165, 130, 1100, 160, "북한산", 8, "C:\\py\\다익스트라\\북한산2.png"),
    ("C:\\py\\다익스트라\\북서울꿈의숲.png", 80, 90, 1280, 240, "북서울꿈의숲", 8, "C:\\py\\다익스트라\\북서울꿈의숲2.png"),
    ("C:\\py\\다익스트라\\도봉산.png", 200, 170, 1170, 30, "도봉산", 0, "C:\\py\\다익스트라\\도봉산2.png"),
    ("C:\\py\\다익스트라\\북악산.png", 145, 100, 1010, 230, "북악산", 8, "C:\\py\\다익스트라\\북악산2.png"),    
    ("C:\\py\\다익스트라\\인왕산.png", 100, 80, 920, 300, "인왕산", 8, "C:\\py\\다익스트라\\인왕산2.png"),
    ("C:\\py\\다익스트라\\롯데타워.png", 40, 150, 1560, 600, "롯데타워", -60, "C:\\py\\다익스트라\\롯데타워2.png"),
    ("C:\\py\\다익스트라\\롯데월드.png", 80, 70, 1520, 700, "롯데월드", 8, "C:\\py\\다익스트라\\롯데월드2.png"),
    ("C:\\py\\다익스트라\\올림픽공원.png", 90, 40, 1610, 650, "올림픽공원", 8, "C:\\py\\다익스트라\\올림픽공원2.png"),
    ("C:\\py\\다익스트라\\암사동유적.png", 90, 40, 1630, 560, "암사동유적", 8, "C:\\py\\다익스트라\\암사동유적2.png"),  
]

# 전역 변수로 저장할 리스트
image_refs = []
button_ids = []
button_states = []
button_text = []

for img_path, width, height, x, y, text, text_offset, new_img_path in button_images:

    # 원래 이미지 로드 및 저장
    original_image = Image.open(img_path)
    original_resized_image = original_image.resize((width, height))
    original_tk_image = ImageTk.PhotoImage(original_resized_image)
    
        # 새 이미지 로드 및 저장
    new_image = Image.open(new_img_path)
    new_resized_image = new_image.resize((width, height))
    new_tk_image = ImageTk.PhotoImage(new_resized_image)
    
    button_states.append('original')  # 버튼의 초기 상태는 원래 이미지

    # Canvas에 클릭 가능한 이미지 생성
    image_id = canvas.create_image(x, y, anchor=tk.NW, image=original_tk_image)
    button_ids.append(image_id)
    
    # 텍스트 추가
    text_id = canvas.create_text(x + width // 2, y + height + text_offset, text=text, font=('Arial', 10, 'bold'))

    button_text.append(text)
    
    # 클릭 이벤트를 이미지에 바인딩
    canvas.tag_bind(image_id, '<Button-1>', on_image_click)
    
    # 이미지 참조 저장 (원래 이미지와 새로운 이미지)
    image_refs.append({
        "original": original_tk_image,
        "new": new_tk_image
    })
    
    

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
        
def update_end_combobox(event, combobox, station_list):
    typed_text = combobox.get()  # 입력된 텍스트 가져오기
    if typed_text == '':
        combobox['values'] = button_text  # 아무 입력이 없으면 전체 리스트
    else:
        # 입력된 텍스트로 시작하는 역들 필터링
        filtered_stations = [text for text in button_text if text.lower().startswith(typed_text.lower())]
        combobox['values'] = filtered_stations  # 필터링된 리스트 적용
        combobox.event_generate('<Down>')  # 첫 번째 항목을 자동으로 선택되도록 설정

# 출발역 라벨과 콤보박스
start_label = tk.Label(left_frame, text="출발역 선택", font=("맑은 고딕", 12))
start_label.pack(padx = 100,pady=20)

start_station_var = tk.StringVar()
start_station_combobox = ttk.Combobox(left_frame, textvariable=start_station_var, state="normal")
start_station_combobox['values'] = station_names  # 모든 역 이름 리스트로 설정
start_station_combobox.pack(pady = 20)


# 출발역 검색 시 자동완성 기능 추가
start_station_combobox.bind('<KeyRelease>', lambda event: update_combobox(event, start_station_combobox, station_names))

# 도착역 라벨과 콤보박스
end_label = tk.Label(left_frame, text="도착 랜드마크 선택", font=("맑은 고딕", 12))
end_label.pack(pady=20)

end_station_var = tk.StringVar()
end_station_combobox = ttk.Combobox(left_frame, textvariable=end_station_var, state="normal")
end_station_combobox['values'] = button_text  # 모든 역 이름 리스트로 설정
end_station_combobox.pack(pady=10)

# 도착역 검색 시 자동완성 기능 추가
end_station_combobox.bind('<KeyRelease>', lambda event: update_end_combobox(event, end_station_combobox, station_names))

# 출발역 텍스트 박스 클릭 시
start_station_combobox.bind('<Button-1>', lambda event: on_textbox_click('start'))

# 도착역 텍스트 박스 클릭 시
end_station_combobox.bind('<Button-1>', lambda event: on_textbox_click('end'))

# 콤보박스에서 항목이 선택되었을 때 실행되는 이벤트 바인딩
start_station_combobox.bind("<<ComboboxSelected>>", lambda event: on_combobox_select(event, 'start'))
end_station_combobox.bind("<<ComboboxSelected>>", lambda event: on_combobox_select(event, 'end'))

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
calculate_button = tk.Button(left_frame, text="최단 시간 계산", command=calculate_shortest_time)
calculate_button.pack(pady=30)

# 결과를 출력할 라벨
result_label = tk.Label(left_frame, text="", font=("맑은 고딕", 12))
result_label.pack(pady=20)
# Tkinter 이벤트 루프 시작
root.mainloop()
