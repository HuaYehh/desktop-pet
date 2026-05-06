import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageSequence
import random
import os

class DesktopPet:
    def __init__(self, image_path):
        self.window = tk.Toplevel()
        
        # 1. 基礎設定：無邊框、置頂
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True)
        
        # 2. 處理 GIF 動畫
        self.frames = []
        self.img_info = Image.open(image_path)
        self.w, self.h = self.img_info.size
        
        # 拆解 GIF 的每一格影格
        for frame in ImageSequence.Iterator(self.img_info):
            # 轉換為 tkinter 可讀取的格式
            # 如果是 GIF，我們保留原圖大小
            # 這裡使用 .copy() 是為了確保每一格都被正確存入記憶體
            photo = ImageTk.PhotoImage(frame.convert("RGBA").copy())
            self.frames.append(photo)
        
        self.frame_index = 0
        self.num_frames = len(self.frames)

        # 3. 使用 Label 顯示第一格
        self.label = tk.Label(self.window, image=self.frames[0], bd=0)
        self.label.pack()

        # 4. 速度與位置設定
        self.x = random.randint(50, 400)
        self.y = random.randint(50, 400)
        self.dx = random.choice([-5, -3, 3, 5]) 
        self.dy = random.choice([-5, -3, 3, 5])

        # 獲取螢幕寬高
        self.screen_w = self.window.winfo_screenwidth()
        self.screen_h = self.window.winfo_screenheight()

        # 滑鼠事件：右鍵點擊（或 Control+左鍵）關閉
        self.window.bind("<Button-2>", lambda e: self.window.destroy()) 
        self.window.bind("<Control-Button-1>", lambda e: self.window.destroy()) 
        
        # 啟動動畫與移動循環
        self.animate()
        self.update_position()

    def animate(self):
        # 切換到下一格影格
        self.frame_index = (self.frame_index + 1) % self.num_frames
        self.label.configure(image=self.frames[self.frame_index])
        
        # 設定動畫速度 (毫秒)，100ms 大約是 10 FPS
        # 如果你的 GIF 跑得太快或太慢，可以調整這個數字
        self.window.after(100, self.animate)

    def update_position(self):
        self.x += self.dx
        self.y += self.dy

        # 碰撞偵測
        if self.x <= 0 or self.x >= self.screen_w - self.w:
            self.dx *= -1
        if self.y <= 0 or self.y >= self.screen_h - self.h:
            self.dy *= -1

        # 更新視窗位置與大小
        self.window.geometry(f"{self.w}x{self.h}+{self.x}+{self.y}")
        self.window.after(10, self.update_position)

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GIF 桌面小精靈")
        self.root.geometry("300x150")
        self.root.eval('tk::PlaceWindow . center')

        tk.Label(root, text="模式：GIF 動畫顯示 (實色原圖)", pady=20).pack()
        tk.Button(root, text="選取 GIF 圖片並開始", command=self.add_pet).pack()

    def add_pet(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("GIF files", "*.gif"), ("All files", "*.*")]
        )
        if file_path:
            DesktopPet(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()