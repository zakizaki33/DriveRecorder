# https://qiita.com/tchnkmr/items/b05f321fa315bbce4f77
# [Python] スレッドで実装する
import shutil
import datetime
import time
import threading


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
threading1 =threading.Thread(target=boil_udon)
threading2 =threading.Thread(target=make_tuyu)

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