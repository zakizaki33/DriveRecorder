# https://qiita.com/tchnkmr/items/b05f321fa315bbce4f77
# [Python] スレッドで実装する
# import shutil
import datetime
import time
import threading
# import os
import tkinter
import cv2
import PIL.Image
import PIL.ImageTk


def boil_udon():
    print("  麺を茹でます")
    time.sleep(3)
    print("麺が茹であがりました")


def make_tuyu():
    print("  つゆを作ります")
    time.sleep(2)
    print("  つゆが出来上がりました")


'''
print("うどんを作ります 1回目")
boil_udon()
make_tuyu()
print("盛り付けます")
print("完成しました")
'''
print("うどんを作ります ２回目")
threading1 = threading.Thread(target=boil_udon)
threading2 = threading.Thread(target=make_tuyu)

# start と　joinをセットにしないと上手く、スレッディングが出来ないのはなんでだ？
threading1.start()
threading2.start()
# joinが無いと待ってくれない
threading1.join()
threading2.join()

print("盛り付けます")
print("完成しました")


'''
# https://note.nkmk.me/python-listdir-isfile-isdir/

# プログラムのプロセスを考える
# 1　フォルダーのリストを取得
# 2 残りの容量をチェックする
# 3 容量OVERの場合、一番古いものを削除する(ファイルないしフォルダーを削除する)

import os
path = "./DATA"
# 勝手に名前順にリストを作ってくれるようだ
list1 = os.listdir(path)
print(list1)
print(list1[0])

dt_now=datetime.datetime.now()
yyyymmdd =dt_now.strftime("%Y%m%d")
print(yyyymmdd)


print  ("    current_directory = os.path.dirname(os.path.abspath(__file__))")
print(os.path.dirname(os.path.abspath(__file__)))
print(os.path.abspath(__file__))

if(not(os.path.exists(yyyymmdd))):
    os.mkdir(yyyymmdd)


# ファイルおよびフォルダを消す作業
# DATAフォルダを作成しておいて、そこに作成された動画がたまっている前提。
# os.remove( path +"/"+ list1[0])
# shutil.rmtree(path + "/" + list1[0])

# https://www.bioerrorlog.work/entry/get-memory-disk-in-python#:~:text=Python%E3%81%AE%E6%A8%99%E6%BA%96%E3%83%A9%E3%82%A4%E3%83%96%E3%83%A9%E3%83%AA%20shutil,%E5%AE%B9%E9%87%8F%E3%82%92%E5%8F%96%E5%BE%97%E3%81%A7%E3%81%8D%E3%81%BE%E3%81%99%E3%80%82
# total, used, free =shutil.disk_usage(path)
total, used, free = shutil.disk_usage("/")

print('---------------------------')
print(f'Total:{total/(10**9)}GB')
print(f'Used:{used/(10**9)}GB')
print(f'Free:{free/(10**9)}GB')

'''

# 【ラズベリーパイ】カメラモジュールの映像をTkinterに表示する方法
# https://yamitomo.com/article/133


class App:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        # 内臓カメラだと０、外付けUSBカメラだと１を入れる
        self.vcap = cv2.VideoCapture(1)

        self.width = int(self.vcap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.vcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.vcap.get(cv2.CAP_PROP_FPS))
        self.fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        '''
        self.name = "video" + datetime.datetime.today().strftime(
            '%Y%m%d_%H%M%S') + ".mp4"
        # 保存名　video + 現在時刻 + .mp4
        self.video = cv2.VideoWriter(
            self.name, self.fourcc, 30.0, (self.width, self.height))
        # (保存名前、fourcc,fps,サイズ)
        '''
        # カメラモジュールの映像を表示するキャンバスを用意する
        self.canvas = tkinter.Canvas(
            window, width=self.width, height=self.height)
        self.canvas.pack()

        # Closeボタン
        self.close_btn = tkinter.Button(window, text="Close")
        self.close_btn.pack()
        self.close_btn.configure(command=self.destructor)

        # update()関数を15ミリ秒ごとに呼び出し、
        # キャンバスの映像を更新する
        self.delay = 15
        self.update()

        self.window.mainloop()

    # キャンバスに表示されているカメラモジュールの映像を
    # 15ミリ秒ごとに更新する
    def update(self):
        # global frame
        # 保存設定回りは関数化できるはず
        self.name = "video" + datetime.datetime.today().strftime(
            '%Y%m%d_%H%M%S') + ".mp4"
        # 保存名　video + 現在時刻 + .mp4
        self.video = cv2.VideoWriter(
            self.name, self.fourcc, 30.0, (self.width, self.height))

        # (保存名前、fourcc,fps,サイズ)

        self.dt_now = datetime.datetime.now()

        '''
        # フォルダの作成
        folder_name = dt_now.strftime('%Y%m%d')
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        video_name = folder_name + "/" + dt_now.strftime(
            '%Y%m%d%H%M%S') + ".mp4"
        print(video_name)
        '''
        # while True:
        # if datetime.datetime.now() < \
        #   (self.dt_now + datetime.timedelta(seconds=5)):

        # 30FPS * 5sec
        # for 文したら、５秒に１回しか画面が更新されない（動画は正常っぽい）
        for num in range(30 * 5):

            # frame　取得
            _, frame = self.vcap.read()

            # 動画保存として、一つの関数にする
            # time.sleep(1 / 1000)  # 1[msec]
            self.video.write(frame)

            # 色調整
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # 画面描画も一つの関数にしたい
            self.im = PIL.Image.fromarray(frame)
            self.photo = PIL.ImageTk.PhotoImage(image=self.im)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

            # create_imageが走っただけではどうやら画面は更新されないようだ
            # https://daeudaeu.com/main_window/
            # https://confrage.jp/python%E3%81%AEtkinter%E3%81%A7gui%E5%85%A5%E9%96%80/
            # self.update()
            self.canvas.update()

        self.window.after(self.delay, self.update)
        print(datetime.datetime.now())

    # Closeボタンの処理
    def destructor(self):
        self.window.destroy()
        self.vcap.release()
        self.video.release()


App(tkinter.Tk(), "Tkinter & Camera module")

'''
# Pythonで指定した時間動画を撮影して保存するプログラム
# https://mayumega.site/prog/py_mv_time/

# 撮影時間を秒で指定  3分の場合は180
time_ = 10

# fpsを20.0にして撮影したい場合はfps=20.0にします
fps = 30.0
cap = cv2.VideoCapture(1)  # USBカメラから映像を撮影、パソコン内蔵カメラの場合は0
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # カメラの幅を取得
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # カメラの高さを取得
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')  # 動画保存時の形式を設定
name = "video" + datetime.datetime.today().strftime('%Y%m%d_%H%M%S') + ".mp4"
# 保存名　video + 現在時刻 + .mp4
video = cv2.VideoWriter(name, fourcc, fps, (w, h))  # (保存名前、fourcc,fps,サイズ)

# fps×指定した撮影時間の値繰り返す
print("start")
roop = int(fps * time_)
for i in range(roop):
    ret, frame = cap.read()  # 1フレーム読み込み
    video.write(frame)  # 1フレーム保存する

print("stop")
video.release()
cap.release()
cv2.destroyAllWindows()
'''
