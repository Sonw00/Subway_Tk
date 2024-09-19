import tkinter as tk

class LineSelectorApp:
    def __init__(self, root):
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()
        
        # 색깔 리스트
        self.colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
        
        # 선 객체 저장을 위한 리스트
        self.lines = []
        
        # 선의 색깔을 원래 색으로 기억하기 위한 딕셔너리
        self.original_colors = {}
        
        # 선택된 선을 추적하기 위한 집합
        self.selected_lines = set()
        
        # 선을 그립니다.
        self.create_lines()
        
        # 클릭 이벤트 핸들러
        self.canvas.bind("<Button-1>", self.on_click)

    def create_lines(self):
        # 선 두께를 4로 설정합니다.
        line_width = 4
        # 지정된 색깔로 선을 그립니다.
        for i, color in enumerate(self.colors):
            y_position = 50 + i * 30  # 선을 수직으로 배열합니다.
            line_id = self.canvas.create_line(50, y_position, 350, y_position, fill=color, width=line_width)
            self.lines.append(line_id)
            self.original_colors[line_id] = color
            # 마우스 오버 및 마우스 나감 이벤트 바인딩
            self.canvas.tag_bind(line_id, "<Enter>", self.on_mouse_enter)
            self.canvas.tag_bind(line_id, "<Leave>", self.on_mouse_leave)

    def on_click(self, event):
        # 클릭한 위치에서 선을 정확히 찾기
        clicked_line_id = self.find_line_at(event.x, event.y)
        
        if clicked_line_id:
            if clicked_line_id in self.selected_lines:
                # 이미 선택된 선을 다시 클릭한 경우, 선택 해제
                self.selected_lines.remove(clicked_line_id)
            else:
                # 새로운 선을 선택한 경우
                self.selected_lines.add(clicked_line_id)
            
            # 클릭된 선을 원래 색으로 유지하고, 나머지 선은 회색으로 변경
            self.update_lines()
        else:
            # 빈 공간을 클릭한 경우 모든 선의 색을 원래대로 돌립니다.
            self.reset_lines()

    def find_line_at(self, x, y):
        # 클릭한 위치에서 선을 정확히 찾기
        for line_id in self.lines:
            coords = self.canvas.coords(line_id)
            if self.is_point_near_line(x, y, coords):
                return line_id
        return None

    def is_point_near_line(self, x, y, coords, tolerance=10):
        # 선과 클릭된 지점 간의 거리 계산
        x1, y1, x2, y2 = coords
        return self.distance_to_line(x, y, x1, y1, x2, y2) < tolerance

    def distance_to_line(self, px, py, x1, y1, x2, y2):
        # 선과 점 간의 최소 거리 계산
        if (x1 == x2) and (y1 == y2):
            return ((px - x1) ** 2 + (py - y1) ** 2) ** 0.5
        else:
            return abs((y2 - y1) * px - (x2 - x1) * py + x2 * y1 - y2 * x1) / ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5

    def update_lines(self):
        # 클릭된 선을 제외한 모든 선의 색을 회색으로 변경
        for line_id in self.lines:
            if line_id in self.selected_lines:
                color = self.original_colors[line_id]  # 클릭된 선의 색상 유지
            else:
                color = 'silver'  # 클릭되지 않은 선의 색상
            self.canvas.itemconfig(line_id, fill=color)

    def reset_lines(self):
        # 클릭된 선은 원래 색상으로 유지하고 나머지 선들은 원래 색상으로 복원
        for line_id in self.lines:
            if line_id not in self.selected_lines:
                self.canvas.itemconfig(line_id, fill=self.original_colors[line_id])
        self.selected_lines.clear()

    def on_mouse_enter(self, event):
        # 마우스가 선 위로 이동할 때 흰색으로 색상 변경
        line_id = self.canvas.find_closest(event.x, event.y)[0]
        if line_id not in self.selected_lines:
            current_fill = self.canvas.itemcget(line_id, 'fill')
            if current_fill != 'silver':  # 회색이 아닌 경우에만 흰색으로 변경
                self.canvas.itemconfig(line_id, fill='white')

    def on_mouse_leave(self, event):
        # 마우스가 선에서 나갈 때 색상 복원
        line_id = self.canvas.find_closest(event.x, event.y)[0]
        if line_id in self.selected_lines:
            # 클릭된 선의 색상 복원
            self.canvas.itemconfig(line_id, fill=self.original_colors[line_id])
        else:
            # 클릭되지 않은 선은 원래 색상으로 복원 (흰색으로 변경되었으면 원래 색상으로 복원)
            if self.canvas.itemcget(line_id, 'fill') == 'white':
                self.canvas.itemconfig(line_id, fill=self.original_colors[line_id])

# Tkinter 애플리케이션 실행
root = tk.Tk()
app = LineSelectorApp(root)
root.mainloop()
