import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # 이미지 처리를 위해 PIL 라이브러리 사용

# 프로젝트 1번 코드 (예시)
def project_1():
    project1_window = tk.Toplevel()
    project1_window.title("Project 1")
    
    label = tk.Label(project1_window, text="This is Project 1")
    label.pack(pady=20)

# 프로젝트 2번 코드 (예시)
def project_2():
    project2_window = tk.Toplevel()
    project2_window.title("Project 2")
    
    label = tk.Label(project2_window, text="This is Project 2")
    label.pack(pady=20)

# 이미지 클릭 이벤트 함수
def on_project_click(project_number):
    if project_number == 1:
        project_1()
    elif project_number == 2:
        project_2()

# 메인 윈도우 생성
root = tk.Tk()
root.title("Project Selector")

x_position = 300
y_position = 200
root.geometry(f"400x200+{x_position}+{y_position}")
root.attributes("-topmost", True)

# 설명 텍스트 추가
l2 = tk.Label(root, text="프로젝트를 선택하세요.")
l2.pack(pady=(10, 15))

# 이미지 로드 (프로젝트에 해당하는 이미지 경로를 입력)
# 이미지는 실제 이미지 파일 경로로 수정해야 함
image1_path = "project1_image.png"  # 프로젝트 1번의 이미지 파일 경로
image2_path = "project2_image.png"  # 프로젝트 2번의 이미지 파일 경로

# PIL로 이미지를 열고, tkinter의 PhotoImage로 변환
img1 = Image.open(image1_path)
img1 = img1.resize((120, 120))  # 이미지 크기 조정
photo1 = ImageTk.PhotoImage(img1)

img2 = Image.open(image2_path)
img2 = img2.resize((120, 120))
photo2 = ImageTk.PhotoImage(img2)

# 이미지 버튼 추가
image1_button = tk.Button(root, image=photo1, command=lambda: on_project_click(1), borderwidth=0)
image1_button.pack(side="left", padx=(50, 10))

image2_button = tk.Button(root, image=photo2, command=lambda: on_project_click(2), borderwidth=0)
image2_button.pack(side="right", padx=(10, 50))

# 메인 루프 실행
root.mainloop()
