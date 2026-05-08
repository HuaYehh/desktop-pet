import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageSequence
import random
import datetime
import os

class DesktopPet:
    def __init__(self, image_path):
        self.window = tk.Toplevel()
        # 1. 基礎設定：無邊框、置頂
        self.window.overrideredirect(True)
        self.window.attributes("-topmost", True) # 關鍵：保持在最上層
        
        # 2. 處理圖片與 GIF
        self.frames = []
        try:
            with Image.open(image_path) as img:
                self.w, self.h = img.size
                for frame in ImageSequence.Iterator(img):
                    photo = ImageTk.PhotoImage(frame.convert("RGB").copy())
                    self.frames.append(photo)
        except Exception as e:
            messagebox.showerror("錯誤", f"讀取失敗：{e}")
            self.window.destroy()
            return
        
        self.frame_index = 0
        self.num_frames = len(self.frames)

        # 3. 顯示標籤
        self.label = tk.Label(self.window, image=self.frames[0], bd=0)
        self.label.pack()

        # 4. 隨機初始位置
        self.x, self.y = random.randint(50, 400), random.randint(50, 400)
        self.dx = random.choice([-5, -3, 3, 5]) 
        self.dy = random.choice([-5, -3, 3, 5])

        self.screen_w = self.window.winfo_screenwidth()
        self.screen_h = self.window.winfo_screenheight()

        # 滑鼠事件：Control+左鍵 關閉
        self.window.bind("<Control-Button-1>", lambda e: self.window.destroy()) 
        
        self.animate()
        self.update_position()

    def animate(self):
        if self.num_frames > 1:
            self.frame_index = (self.frame_index + 1) % self.num_frames
            self.label.configure(image=self.frames[self.frame_index])
            self.window.after(100, self.animate)

    def update_position(self):
        self.x += self.dx
        self.y += self.dy

        if self.x <= 0 or self.x >= self.screen_w - self.w: self.dx *= -1
        if self.y <= 0 or self.y >= self.screen_h - self.h: self.dy *= -1

        # 更新座標
        self.window.geometry(f"{self.w}x{self.h}+{self.x}+{self.y}")
        
        # --- 強化置頂核心：每次移動時都強制往最上層提 ---
        self.window.lift() 
        self.window.attributes("-topmost", True)
        
        self.window.after(10, self.update_position)

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("動態精靈召喚器")
        self.root.geometry("350x270")
        self.root.eval('tk::PlaceWindow . center')

        self.selected_file = ""

        tk.Label(root, text="Step 1: 先選取小精靈圖片 (GIF/PNG/JPG)", pady=5).pack()
        self.file_label = tk.Label(root, text="尚未選取檔案", font=("Arial", 10, "bold"))
        self.file_label.pack(pady=5)
        tk.Button(root, text="瀏覽檔案", command=self.select_file).pack()

        tk.Label(root, text="Step 2: 設定幾分鐘後自動開啟", pady=10).pack()
        self.minute_entry = tk.Entry(root, width=12, justify='center')
        self.minute_entry.insert(0, "1")
        self.minute_entry.pack()

        self.start_btn = tk.Button(root, text="開始倒數計時", command=self.start_timer, fg="white", bg="#4CAF50")
        self.start_btn.pack(pady=15)

        self.status_label = tk.Label(root, text="等待設定中...", fg="blue")
        self.status_label.pack(pady=5)

    def select_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.selected_file = file_path
            self.file_label.config(text=os.path.basename(file_path))

    def start_timer(self):
        if not self.selected_file:
            messagebox.showwarning("提示", "請先選取圖片！")
            return
        try:
            mins = float(self.minute_entry.get())
            now = datetime.datetime.now()
            target_time = now + datetime.timedelta(minutes=mins)
            self.status_label.config(text=f"將於 {target_time.strftime('%H:%M:%S')} 開啟", fg="#007bff")
            self.root.after(int(mins * 60 * 1000), lambda: DesktopPet(self.selected_file))
        except:
            messagebox.showerror("錯誤", "請輸入有效的數字")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()