import datetime
import tkinter
import cv2
import PIL.Image
import PIL.ImageTk


class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        # 内臓カメラだと０、外付けUSBカメラだと１を入れる
        # self.vcap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.vcap = cv2.VideoCapture(0)

        # VideoCapture VideoWriter の画面サイズが合っていないと上手く動画が保存できない
        self.width = int(self.vcap.get(cv2.CAP_PROP_FRAME_WIDTH)/2)  # default 640
        self.height = int(self.vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)/2) # default 320
        self.fps = int(self.vcap.get(cv2.CAP_PROP_FPS))
        self.fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

        # カメラモジュールの映像を表示するキャンバスを用意する
        self.canvas = tkinter.Canvas(
            window, width=self.width, height=self.height)
        self.canvas.pack(fill='x', side='left')

        # STARTボタン
        self.start_btn = tkinter.Button(window, text="START")
        # self.start_btn.pack()
        self.start_btn.pack(fill='x', side='top')
        self.start_btn.configure(command=self.update)
        self.start_btn.configure(width=20, height=5)

        # Closeボタン
        self.close_btn = tkinter.Button(window, text="Close")
        # self.close_btn.pack()
        self.close_btn.pack(fill='x', side='top')
        self.close_btn.configure(command=self.destructor)
        self.close_btn.configure(width=20, height=5)

        # update()関数を15ミリ秒ごとに呼び出し、キャンバスの映像を更新する
        self.delay = 15
        # self.update()

        # 無限ループ
        self.window.mainloop()

    # キャンバスに表示されているカメラモジュールの映像を15ミリ秒ごとに更新する
    def update(self):
        self.name = "video" + datetime.datetime.today().strftime(
            '%Y%m%d_%H%M%S') + ".mp4"
        self.video = cv2.VideoWriter(
            # self.name, self.fourcc, 30.0, (self.width, self.height))
            self.name, self.fourcc, 30.0, (640, 480))
        # (保存名前、fourcc,fps,サイズ)

        # 30FPS * 5sec
        for num in range(30 * 5):
            # frame　取得
            _, frame = self.vcap.read()
            self.video.write(frame)

            # 色調整
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.im = PIL.Image.fromarray(frame)
            self.photo = PIL.ImageTk.PhotoImage(image=self.im)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
            self.canvas.update()  # create_imageが走っただけではどうやら画面は更新されないようだ

        self.window.after(self.delay, self.update)
        print(datetime.datetime.now())

    # Closeボタンの処理
    def destructor(self):
        self.video.release()
        self.vcap.release()
        self.window.destroy()


App(tkinter.Tk(), "Tkinter & USB Camera")

# 【参考ページ】
# ①【ラズベリーパイ】カメラモジュールの映像をTkinterに表示する方法
# https://yamitomo.com/article/133

# ②Canvasのアップデート
# https://daeudaeu.com/main_window/
# https://confrage.jp/python%E3%81%AEtkinter%E3%81%A7gui%E5%85%A5%E9%96%80/
