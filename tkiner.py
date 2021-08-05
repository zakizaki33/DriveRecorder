import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)

        self.master.geometry("250x250") 

        # ボタンの作成
        button_top = tk.Button(self.master, text = "TOP", width = 8)
        button_bottom = tk.Button(self.master, text = "BOTTOM", width = 8)
        button_left = tk.Button(self.master, text = "LEFT", width = 8)
        button_right = tk.Button(self.master, text = "RIGHT", width = 8)

        # ウィジェットの配置
        button_top.pack(side = tk.TOP)
        button_bottom.pack(side = tk.BOTTOM)
        button_left.pack(side = tk.LEFT)
        button_right.pack(side = tk.RIGHT)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master = root)
    app.mainloop()