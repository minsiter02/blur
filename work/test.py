import tkinter as tk

class DragRectangleApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=500, height=400, bg="white")
        self.canvas.pack()

        self.start_x = None
        self.start_y = None
        self.rect = None

        # 마우스 이벤트 바인딩
        self.canvas.bind("<ButtonPress-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        """마우스를 누를 때 시작 좌표 저장"""
        self.start_x = event.x
        self.start_y = event.y
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="blue", width=2)

    def on_drag(self, event):
        """드래그 중일 때 사각형 크기 업데이트"""
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        """드래그 완료 후 최종 좌표 설정"""
        self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

# Tkinter 실행
root = tk.Tk()
app = DragRectangleApp(root)
root.mainloop()