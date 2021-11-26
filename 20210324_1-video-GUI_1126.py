import tkinter as tk
import cv2
import PIL.Image
import PIL.ImageTk
import datetime
import shutil
import os
import threading
import sys


class Application(tk.Frame):

    flag = 0
    
    # 内蔵カメラの時は0,外付けUSBカメラの時は1にする
    def __init__(self, master, video_source=0):
        super().__init__(master)

        # ---------------------------------------------------------
        # setting_window
        # ---------------------------------------------------------
        self.master.geometry("300x300")
        self.master.title("Tkinter with Video Streaming and Capture")

        # ---------------------------------------------------------
        # Open the video source
        # https://note.nkmk.me/python-opencv-videocapture-file-camera/
        # ---------------------------------------------------------
        self.vcap = cv2.VideoCapture(video_source, cv2.CAP_DSHOW)  # 21-11-26追記

        if self.vcap.isOpened() is False:
            print("There is no Camera")
            sys.exit()

        self.width = self.vcap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.fps = int(self.vcap.get(cv2.CAP_PROP_FPS))

        # ---------------------------------------------------------
        # Widget
        # ---------------------------------------------------------
        self.create_widgets()

        # ---------------------------------------------------------
        # Canvas Update
        # ---------------------------------------------------------
        self.delay = 30  # millisecond
        self.threading1 = threading.Thread(target=self.update)
        # https://blog.novonovo.jp/python/%E3%82%AD%E3%83%A5%E3%83%BC%E3%81%A8%E3%82%B9%E3%83%AC%E3%83%83%E3%83%89/
        self.threading1.setDaemon(True)
        self.threading1.start()
        # self.update()  # ここで描画する

    # ---------------------------------------------------------
    # Create Widget
    # https://www.shido.info/py/tkinter2.html
    # ---------------------------------------------------------
    def create_widgets(self):
        # Frame_Camera
        self.frame_cam = tk.LabelFrame(
            self.master, text='Camera')
        self.frame_cam.place(
            x=10, y=10)
        self.frame_cam.configure(
            width=self.width + 30, height=self.height + 50)
        self.frame_cam.grid_propagate(0)

        # Canvas
        self.canvas1 = tk.Canvas(self.frame_cam)
        self.canvas1.configure(width=self.width, height=self.height)
        self.canvas1.grid(column=0, row=0, padx=10, pady=10)

        # label
        text1 = "録画停止中"
        self.words1 = tk.Label(text=text1, font=("", 24))
        self.words1.place(x=800, y=100)
        self.words2 = tk.Label(text=text1, font=("", 36))
        self.words2.place(x=800, y=200)

        # Frame_Button
        self.frame_btn = tk.LabelFrame(self.master, text='Control')
        self.frame_btn.place(x=10, y=550)
        self.frame_btn.configure(width=self.width + 30, height=120)
        self.frame_btn.grid_propagate(0)

        # Snapshot Button
        # ボタンが押された時に、press_snapshot_button を発動する
        self.btn_snapshot = tk.Button(self.frame_btn, text='録画スタート だよ')
        self.btn_snapshot.configure(
            width=15, height=1, command=self.press_snapshot_button)
        self.btn_snapshot.grid(column=0, row=0, padx=20, pady=10)
     
        # Close Button
        self.btn_close = tk.Button(self.frame_btn, text='Close')
        self.btn_close.configure(
            width=15, height=1, command=self.press_close_button)
        self.btn_close.grid(column=1, row=0, padx=20, pady=10)

    def update(self):
        # Get a frame from the video source
        # https://qiita.com/kotai2003/items/3d31528d56059c848458
        _, frame = self.vcap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        self.canvas1.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.master.after(self.delay, self.update)

    def press_snapshot_button(self):
        self.words2["text"] = "snapshot_button pushed!!!"
        # 録画スタート
        # スレッドではなくて、プロセスを使うらしい？
        # https://qiita.com/ttiger55/items/5e1d5a3405d2b3ef8f40
        
        self.threading2 = threading.Thread(target=self.video_recode)
        self.threading2.setDaemon(True)
        self.threading2.start()
        # threading.Thread(target=self.video_recode).start()
        # ↓録画をうまく開始できないので一旦消す。　★★★
        # Process(target=self.video_recode).start()
        # Process(target=test111).start()
        # ppp= Process(target=test111)
        # ppp.start()

        # flag の値に応じて、ボタンに表記される文言を変える
        # https://www.delftstack.com/ja/howto/python-tkinter/how-to-change-the-tkinter-button-text/

        if (self.flag == 0):
            self.btn_snapshot.configure(text="STOP だよ")
            self.words1.configure(text="録画実行中")
            self.flag = 1
        else:
            self.btn_snapshot.configure(text="録画START だよ")
            self.words1.configure(text="録画停止中")
            self.flag = 0

    def press_close_button(self):
        # self.threading1.join()  # スレッドの後片付け
        # self.threading2.join()
        
        self.vcap.release()
        self.video.release()
        self.master.destroy()
        sys.exit()
        # 終了処理が美しくないが、まずは良しとしたい

    def video_recode(self):
        # ビデオ入力取得（applicationクラスでなんとかならないか。。。）
        w = self.vcap.get(cv2.CAP_PROP_FRAME_WIDTH)
        h = self.vcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fps = int(self.vcap.get(cv2.CAP_PROP_FPS))
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')

        dt_now = datetime.datetime.now()

        # 古い動画の削除
        yesterday = dt_now - datetime.timedelta(days=1)
        try:
            shutil.rmtree(yesterday.strftime('%Y%m%d'))
        except OSError as err:
            print("OS error: {0}".format(err))
            print("削除するべきフォルダーはありません")

        # フォルダの作成
        folder_name = dt_now.strftime('%Y%m%d')
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)

        while True:
            dt_now = datetime.datetime.now()
            video_name = folder_name + "/" + dt_now.strftime(
                '%Y%m%d%H%M%S') + ".mp4"
            print(video_name)

            # 動画ファイルの保存
            # 動画の仕様（ファイル名、fourcc, FPS, サイズ）
            self.video = cv2.VideoWriter(
                video_name, fourcc, fps, (int(w), int(h)))
            # 動画の保存処理
        
            count = 0
            while True:
                _, frame = self.vcap.read()
                self.video.write(frame)        # 動画を1フレームずつ保存する

                count = count + 1
                if count == (fps * 15):   # なんでかよくわからないが21secごとになる
                    break


def main():
    root = tk.Tk()
    app = Application(master=root)  # Inherit
    app.mainloop()

    
if __name__ == "__main__":
    main()
 
