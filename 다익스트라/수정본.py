import tkinter as tk
from PIL import Image, ImageTk

def on_image_click(event):
    image_id = event.widget.find_withtag('current')[0]
    print(f"{image_id} image clicked!")
    toggle_image(image_id)

def toggle_image(image_id):
    global image_refs, button_images, button_ids, button_states

    # 버튼 이미지 정보를 가져옵니다
    button_index = button_ids.index(image_id)
    img_path, width, height, x, y, text, text_offset, new_img_path = button_images[button_index]

    # 현재 상태를 확인합니다
    current_state = button_states[button_index]
    
    if current_state == 'original':
        # 교체할 이미지로 전환
        new_button_image = Image.open(new_img_path)
        new_button_resized_image = new_button_image.resize((width, height))
        new_button_tk_image = ImageTk.PhotoImage(new_button_resized_image)
        canvas.itemconfig(image_id, image=new_button_tk_image)
        image_refs[button_index] = new_button_tk_image
        button_states[button_index] = 'new'
    else:
        # 원래 이미지로 돌아가기
        original_image = Image.open(img_path)
        original_resized_image = original_image.resize((width, height))
        original_tk_image = ImageTk.PhotoImage(original_resized_image)
        canvas.itemconfig(image_id, image=original_tk_image)
        image_refs[button_index] = original_tk_image
        button_states[button_index] = 'original'

# 메인 윈도우 생성
root = tk.Tk()
root.title("Subway")

# Canvas 위젯 생성
canvas = tk.Canvas(root, width=1900, height=1100, background="darkgray")
canvas.pack()

# 배경 이미지 로드 및 크기 조정
background_image_path = "C:\\py\\다익스트라\\지도찐최종.png"  # 이미지 파일 경로를 바꾸세요
background_image = Image.open(background_image_path)
background_image_resized = background_image.resize((2200, 1100))
background_tk_image = ImageTk.PhotoImage(background_image_resized)

# Canvas에 배경 이미지 표시
canvas.create_image(0, 0, anchor=tk.NW, image=background_tk_image)

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

for img_path, width, height, x, y, text, text_offset, new_img_path in button_images:
    button_image = Image.open(img_path)
    button_resized_image = button_image.resize((width, height))
    button_tk_image = ImageTk.PhotoImage(button_resized_image)
    
    # 전역 변수에 저장
    image_refs.append(button_tk_image)
    button_states.append('original')  # 버튼의 초기 상태는 원래 이미지

    # Canvas에 클릭 가능한 이미지 생성
    image_id = canvas.create_image(x, y, anchor=tk.NW, image=button_tk_image)
    button_ids.append(image_id)
    
    # 텍스트 추가
    text_id = canvas.create_text(x + width // 2, y + height + text_offset, text=text, font=('Arial', 10, 'bold'))

    # 클릭 이벤트를 이미지에 바인딩
    canvas.tag_bind(image_id, '<Button-1>', on_image_click)

# Tkinter 이벤트 루프 시작
root.mainloop()
