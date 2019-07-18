#!/usr/bin/python
# -*- coding: UTF-8 -*-

# https://docs.python.org/zh-cn/3/library/tkinter.html
import os
import tkinter as tk

# filedialog是tkinter的一个模块而不是函数,所以必须用import引入
# import tkinter.filedialog as filedialog
from tkinter import filedialog

from tkinter import ttk
from tkinter import messagebox


def batch_rename(path, name):
    name_type = os.path.splitext(name)[-1]

    if name_type == '':
        messagebox.showwarning('错误', '缺少文件类型,示例:doc,docx,xls,xlsx,jpg');
        return ''

    if name.find('%d') == -1:
        name = name.replace(name_type, '-%d' + name_type)

    path = path.replace('\\', '/').rstrip('/')

    num = 1
    script = __file__

    message = ''
    for root, dirs, files in os.walk(path):
        for file in files:
            file_new = name % (num,)
            if path + '/' + file == script:
                continue
            if file.lower().find(name_type) == -1:
                continue
            os.rename(path + '/' + file, path + '/' + file_new)
            message += "\"%s\" 改名为 \"%s\" | " % (file, file_new)
            num += 1
    return message, num


# 第1步，实例化object，建立窗口window
window = tk.Tk()

# 第2步，给窗口的可视化起名字
window.title('批量改名')


def set_win_center(root, curWidth=200, curHight=200):
    '''
    设置窗口大小，并居中显示
    :param root:主窗体实例
    :param curWidth:窗口宽度，非必填，默认200
    :param curHight:窗口高度，非必填，默认200
    :return:无
    '''
    if not curWidth:
        '''获取窗口宽度，默认200'''
        curWidth = root.winfo_width()
    if not curHight:
        '''获取窗口高度，默认200'''
        curHight = root.winfo_height()
    # print(curWidth, curHight)

    # 获取屏幕宽度和高度
    scn_w, scn_h = root.maxsize()
    # print(scn_w, scn_h)

    # 计算中心坐标
    cen_x = (scn_w - curWidth) / 2
    cen_y = (scn_h - curHight) / 2
    # print(cen_x, cen_y)

    # 设置窗口初始大小和位置
    size_xy = '%dx%d+%d+%d' % (curWidth, curHight, cen_x, cen_y)
    root.geometry(size_xy)


# 第3步，设定窗口的大小(长 * 宽)
# window.geometry('500x300')  # 这里的乘是小x
set_win_center(window, 500, 250)

# 第4步，在图形界面上设定标签
l = tk.Label(window, text='批量改名', bg='#f0f0f0', font=('黑体', 16), height=1)
# 说明： bg为背景，font为字体，width为长，height为高，这里的长和高是字符的长和高，比如height=2,就是标签有2个字符这么高

# 第5步，放置标签
l.pack(fill='x')  # Label内容content区域放置位置，自动调节尺寸
# 放置lable的方法有：1）l.pack(); 2)l.place();


tk.Label(window, text='1.输入需改名文件的目录,不填写为当前目录.', bg='#f0f0f0', font=('黑体', 12)).pack(fill='x', pady=0, ipady=0)
tk.Label(window, text='2.输入需改为的名称,格式为"名称-%d.类型",%d代表序号.', bg='#f0f0f0', font=('黑体', 12)).pack(fill='x', pady=0, ipady=0)

path_var = tk.StringVar()
path_var.set(os.getcwd())
path_entry = ttk.Entry(window, textvariable=path_var, font=('微软雅黑', 12))
path_entry.pack(ipadx=80)


def select_path():
    path = filedialog.askdirectory()
    if path != '':
        path_var.set(path)


ttk.Button(window, text='选择文件夹', command=select_path).pack()

name_var = tk.StringVar()
name_var.set('file-%d.txt')
name_entry = ttk.Entry(window, textvariable=name_var, font=('微软雅黑', 12))
name_entry.pack(ipadx=80)


def begin_handle():
    messages, num = batch_rename(path_var.get(), name_var.get())
    messagebox.showinfo('提示', "修改%d个文件名称" % (num - 1,))


ttk.Button(window, text='批量修改', command=begin_handle).pack()


def callback():
    messagebox.showinfo('作者', '悠悠山雨')


# 创建一个顶级菜单
menubar = tk.Menu(window)

# 创建一个下拉菜单“文件”，然后将它添加到顶级菜单中
filemenu = tk.Menu(menubar, tearoff=False)
filemenu.add_command(label="选择文件夹", command=select_path)
filemenu.add_command(label="批量修改", command=begin_handle)
filemenu.add_separator()
filemenu.add_command(label="退出", command=window.quit)
menubar.add_cascade(label="文件", menu=filemenu)

# 创建另一个下拉菜单“编辑”，然后将它添加到顶级菜单中
editmenu = tk.Menu(menubar, tearoff=False)
editmenu.add_command(label="作者", command=callback)
menubar.add_cascade(label="关于", menu=editmenu)

# 显示菜单
window.config(menu=menubar)

# 第6步，主窗口循环显示
window.mainloop()
# 注意，loop因为是循环的意思，window.mainloop就会让window不断的刷新，如果没有mainloop,就是一个静态的window,传入进去的值就不会有循环，mainloop就相当于一个很大的while循环，有个while，每点击一次就会更新一次，所以我们必须要有循环
# 所有的窗口文件都必须有类似的mainloop函数，mainloop是窗口文件的关键的关键。
