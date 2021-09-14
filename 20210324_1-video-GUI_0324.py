import tkinter as tk
# from tkinter import ttk
import cv2
import PIL.Image
import PIL.ImageTk
from tkinter import font
import datetime
# import time
import shutil
import os
import threading
import sys
# from multiprocessing import Process
import platform
import logging
logging.basicConfig(filename="test.log", level=logging.DEBUG)


class Application(tk.Frame):

    flag = 0
    
    # 内蔵カメラの時は0,外付けUSBカメラの時は1にする
    def __init__(self, master, video_source=0):
        super().__init__(master)

        # ---------------------------------------------------------
        # clean_folder
        # ---------------------------------------------------------
        self.clean_folder()

        # ---------------------------------------------------------
        # setting_window
        # ---------------------------------------------------------
        self.master.geometry("700x700")
        self.master.title("Tkinter with Video Streaming and Capture")

        # ---------------------------------------------------------
        # Font
        # ---------------------------------------------------------
        self.font_frame = font.Font(
            family="Meiryo UI", size=15, weight="normal")
        self.font_btn_big = font.Font(
            family="Meiryo UI", size=20, weight="bold")
        self.font_btn_small = font.Font(
            family="Meiryo UI", size=15, weight="bold")

        self.font_lbl_bigger = font.Font(
            family="Meiryo UI", size=45, weight="bold")
        self.font_lbl_big = font.Font(
            family="Meiryo UI", size=30, weight="bold")
        self.font_lbl_middle = font.Font(
            family="Meiryo UI", size=15, weight="bold")
        self.font_lbl_small = font.Font(
            family="Meiryo UI", size=12, weight="normal")

        # ---------------------------------------------------------
        # Open the video source
        # https://note.nkmk.me/python-opencv-videocapture-file-camera/
        # ---------------------------------------------------------
        self.vcap = cv2.VideoCapture(video_source)

        logging.debug(datetime.datetime.now())
        logging.debug(type(self.vcap))
        logging.debug(self.vcap.isOpened())
        if self.vcap.isOpened() is False:
            logging.info("There is no Camera")
            # self.var = tk.StringVar()
            # self.var.set("There is no Camera")
            # self.words1 = tk.Label(textvariable=self.var, font=("", 12))
            # self.words1.pack()
            # time.sleep(3)
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
        self.threading1.start()
        # self.update()  # ここで描画する

    # ---------------------------------------------------------
    # Create Widget
    # https://www.shido.info/py/tkinter2.html
    # ---------------------------------------------------------
    def create_widgets(self):
        # Frame_Camera
        self.frame_cam = tk.LabelFrame(
            self.master, text='Camera', font=self.font_frame)
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
        self.frame_btn = tk.LabelFrame(
            self.master, text='Control', font=self.font_frame)
        self.frame_btn.place(x=10, y=550)
        self.frame_btn.configure(width=self.width + 30, height=120)
        self.frame_btn.grid_propagate(0)

        # Snapshot Button
        # ボタンが押された時に、press_snapshot_button を発動する
        self.btn_snapshot = tk.Button(
            self.frame_btn, text='録画スタート だよ', font=self.font_btn_big)
        self.btn_snapshot.configure(
            width=15, height=1, command=self.press_snapshot_button)
        self.btn_snapshot.grid(column=0, row=0, padx=20, pady=10)
        logging.info("snap button created !!! ")
     
        # Close Button
        self.btn_close = tk.Button(
            self.frame_btn, text='Close', font=self.font_btn_big)
        self.btn_close.configure(
            width=15, height=1, command=self.press_close_button)
        self.btn_close.grid(column=1, row=0, padx=20, pady=10)
        logging.info("close button created !!! ")

    def update(self):
        # Get a frame from the video source
        # https://qiita.com/kotai2003/items/3d31528d56059c848458
        _, frame = self.vcap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))

        # self.photo -> Canvas
        self.canvas1.create_image(0, 0, image=self.photo, anchor=tk.NW)
        self.master.after(self.delay, self.update)

    def press_snapshot_button(self):
        # ラベルにログを表示させる
        logging.info("snapshot_button pushed!!!")
        # self.var.set("snapshot_button pushed!!!")
        self.words2["text"] = "snapshot_button pushed!!!"
        # 録画スタート
        # スレッドではなくて、プロセスを使うらしい？
        # https://qiita.com/ttiger55/items/5e1d5a3405d2b3ef8f40
        
        self.threading2 = threading.Thread(target=self.video_recode)
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
            # self.t1.start()
            self.btn_snapshot.configure(text="STOP だよ")
            self.words1.configure(text="録画実行中")
            self.flag = 1
        else:
            self.btn_snapshot.configure(text="録画START だよ")
            self.words1.configure(text="録画停止中")
            self.flag = 0

    def press_close_button(self):
        self.threading1.join()  # スレッドの後片付け
        self.master.destroy()
        self.vcap.release()

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
            logging.error("OS error: {0}".format(err))
            # print("NONONO")
            logging.error("NONONO")

        # フォルダの作成
        folder_name = dt_now.strftime('%Y%m%d')
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)

        video_name = folder_name + "/" + dt_now.strftime(
            '%Y%m%d%H%M%S') + ".mp4"
        print(video_name)
        logging.error(video_name)

        # 動画ファイルの保存
        # 動画の仕様（ファイル名、fourcc, FPS, サイズ）
        video = cv2.VideoWriter(video_name, fourcc, fps, (int(w), int(h)))
        # 動画の保存処理
        count = 0
        while True:
            _, frame = self.vcap.read()
            video.write(frame)        # 動画を1フレームずつ保存する

            count = count + 1
            if count == (fps * 15):
                break
            
    def clean_folder(self):
        path = "./"
        # 勝手に名前順にリストを作ってくれるようだ
        list1 = os.listdir(path)
        print(path)
        print(list1)
        print(list1[0])

        # https://blog.codecamp.jp/python-list
        # リストの中身を確認して、todayより古ければ削除する（文字数も８文字である事を同時の考慮？）
        for i in list1:
            print(i)
            print(len(i))
            dt_now = datetime.datetime.now()
            yesterday = dt_now - datetime.timedelta(days=1)
            print(yesterday.strftime('%Y%m%d'))
            if(len(i) == 8 and i < yesterday.strftime('%Y%m%d')):
                
                total, used, free = shutil.disk_usage("/")
                print('-------Data Check--------------------')
                print(f'Free:{free/(10**9)}GB')
                #  残ディスク容量を決める
                if(252.220 > free / (10**9)):
                    print("folder delete")
                    shutil.rmtree(
                        os.path.dirname(os.path.abspath(__file__)) + "/" + i)
                    # shutil.rmtree(yesterday.strftime('%Y%m%d'))

        dt_now = datetime.datetime.now()
        yyyymmdd = dt_now.strftime("%Y%m%d")
        print(yyyymmdd)

        print("current_directory = os.path.dirname(os.path.abspath(__file__))")
        print(os.path.dirname(os.path.abspath(__file__)))
        print(os.path.abspath(__file__))


def main():
    root = tk.Tk()
    
    # ---------------------------------------------------------
    # setting platform (Windows or Linux)
    # http://utisam.hateblo.jp/entry/2013/01/12/212958
    # ---------------------------------------------------------
    if platform.system() == "Windows":
        root.state('zoomed')  # when windows
    else:
        root.attributes("-zoomed", "1")  # when Linux & Mac

    app = Application(master=root)  # Inherit
    app.mainloop()

    
if __name__ == "__main__":
    logging.info("main start!!!")
    main()
 
