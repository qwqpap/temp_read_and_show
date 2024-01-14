import serial
import numpy
import tkinter as tk
from threading import Thread
import time
from matplotlib import pyplot as plt
ser = serial.Serial('COM3', 115200, timeout=5)
temp_list = [27, 27, 27, 27, 27, 27, 27, 27]
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
x = [1]
y = [0]
plt.ion()
plt.title("历史最大温差",loc="left")
# 添加图例
plt.xlabel("采样次数",size=8)
plt.ylabel("温差（摄氏度）",size=8)
def got_temp(res):
    B_VALUE = 4300
    TEMP_1 = 273.15 + 25.00
    res = 1 / ((numpy.log(res / 100)) / B_VALUE + (1 / TEMP_1))
    res = res - 273.15
    return res
i = 1


def update_display():
    # 更新温度显示
    global i
    i = i +1
    label0.config(text="temp_1:"+str(temp_list[0]))
    label1.config(text="temp_2:"+str(temp_list[1]))
    label2.config(text="temp_3:"+str(temp_list[2]))
    label3.config(text="temp_4:"+str(temp_list[3]))
    label4.config(text="temp_5:"+str(temp_list[4]))
    label5.config(text="temp_6:"+str(temp_list[5]))
    label6.config(text="temp_7:"+str(temp_list[6]))
    label7.config(text="temp_8:"+str(temp_list[7]))
    #label8.config(text=(max(temp_list)-min(temp_list)))
    y.append(max(temp_list)-min(temp_list))
    # 每隔一段时间调用update_display函数
    plt.clf()  # 清除之前画的图
    x.append(i)
    plt.plot(x, y)  # 画出当前x列表和y列表中的值的图形
    plt.title("实时最大温差", loc="center")
    # 添加图例
    plt.xlabel("采样次数", size=12)
    plt.ylabel("温差（摄氏度）", size=12)
    plt.pause(0.001)  # 暂停一段时间，不然画的太快会卡住显示不出来
    plt.ioff()  # 关闭画图窗口
    root.after(1, update_display)


def serial_read():
    while True:
        # time.sleep(0.05)
        now_data = ser.readline()
        now_data = str(now_data)
        now_data = now_data[2:7]

        try:
            chanel = int(int(now_data) / 10000)
            now_data = int(now_data) - chanel * 10000
            if chanel != 0:
                now_res = 100 * (now_data / (4095 - now_data))
                tep_now = got_temp(now_res)
                temp_list[chanel - 1] = tep_now
        except:
            print("not_complete_data")

# 创建主窗口
root = tk.Tk()
root.title("温度显示")

# 创建标签用于显示温度数据
label0 = tk.Label(root, text=temp_list[0])
label1 = tk.Label(root, text=temp_list[1])
label2 = tk.Label(root, text=temp_list[2])
label3 = tk.Label(root, text=temp_list[3])
label4 = tk.Label(root, text=temp_list[4])
label5 = tk.Label(root, text=temp_list[5])
label6 = tk.Label(root, text=temp_list[6])
label7 = tk.Label(root, text=temp_list[7])
#label8 = tk.Label(root,text=(max(temp_list)-min(temp_list)))
tk.Label(root, text='声波制冷效应各传感器温度', font=('Arial',20)).pack()
label0.pack()
label1.pack()
label2.pack()
label3.pack()
label4.pack()
label5.pack()
label6.pack()
label7.pack()
#label8.pack()
# 启动串口读取线程
serial_thread = Thread(target=serial_read)
serial_thread.daemon = True
serial_thread.start()

# 启动数据更新
update_display()

# 进入主循环
root.mainloop()

