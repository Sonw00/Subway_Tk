import tkinter as tk
from tkinter import ttk  # Import ttk for combobox
from PIL import Image, ImageTk

def on_click(event):
    """마우스 클릭 이벤트 핸들러"""
    # 클릭한 좌표를 터미널에 출력
    print(f"클릭 좌표: x={event.x}, y={event.y}")

# Tkinter 윈도우 생성
root = tk.Tk()
root.title("이미지 표시 예제")

# 좌우 프레임 생성
left_frame = tk.Frame(root, width=1300, height=1100)  # 이미지 크기에 맞게 설정
right_frame = tk.Frame(root, width=400, height=1100)

left_frame.grid(row=0, column=0, padx=0, pady=0, sticky='nsew')
right_frame.grid(row=0, column=1, padx=0, pady=0, sticky='nsew')

# 이미지 열기
image_path = "C:\\Users\\2C000013\\Desktop\\수도권지하철노선도.png"  # 이미지 파일 경로를 지정하세요
image = Image.open(image_path)

# 이미지 리사이즈
resized_img = image.resize((1300, 1100), Image.LANCZOS)
photo = ImageTk.PhotoImage(resized_img)

# Label 위젯을 사용하여 이미지 표시
label = tk.Label(left_frame, image=photo)
label.pack(fill=tk.BOTH, expand=True)

# 마우스 클릭 이벤트 핸들러 등록
label.bind("<Button-1>", on_click)

# 출발역 라벨과 콤보박스
start_label = tk.Label(right_frame, text="출발역 선택", font=("맑은 고딕", 12))
start_label.pack(padx=20, pady=10)

start_station_var = tk.StringVar()
start_station_combobox = ttk.Combobox(right_frame, textvariable=start_station_var, state="")
start_station_combobox['values'] = ["역1", "역2", "역3"]  # 예시 역 이름
start_station_combobox.pack(pady=100)

# 도착역 라벨과 콤보박스
end_label = tk.Label(right_frame, text="도착역 선택", font=("맑은 고딕", 12))
end_label.pack(pady=10)

end_station_var = tk.StringVar()
end_station_combobox = ttk.Combobox(right_frame, textvariable=end_station_var, state="")
end_station_combobox['values'] = ["역1", "역2", "역3"]  # 예시 역 이름
end_station_combobox.pack(pady=10)

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

# 메인 루프 실행
root.mainloop()
