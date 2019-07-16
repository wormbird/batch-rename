#!/usr/bin/python
# -*- coding: UTF-8 -*-

# pyinstaller -y -F -i "D:/Python/rename.ico"  "D:/Python/rename.py"

import os, sys, signal


def sigint_handler(signal_num, frame):
    print("使用Ctrl+C退出程序")
    sys.exit(signal_num)


signal.signal(signal.SIGINT, sigint_handler)


def user_input_params():
    print("批量改名使用说明:")
    path = os.getcwd()
    print("1.输入需改名文件的目录,不填写为当前目录. (默认: %s)" % (path,))
    name = 'file-%d.txt'
    name_type = '.txt'
    print("2.输入需改为的名称,格式为\"名称-%%d.类型\",%%d代表序号. (默认: %s)" % (name,))

    while True:
        user_path = input("请输入目录: ")
        if user_path != '':
            path = user_path
        path = path.replace('\\', '/').rstrip('/')
        print("指定目录: %s" % (path,))

        user_name = input("请输入名称: ")
        if user_name != '':
            name_type = os.path.splitext(user_name)[-1]
            if user_name.find('%d') == -1:
                user_name = user_name.replace(name_type, '-%d' + name_type)
            name = user_name
        print("指定名称: %s" % (name,))

        is_confirm = input("是否确认? [Y/n]")
        if is_confirm == '' or is_confirm == 'Y' or is_confirm == 'y':
            break

    return path, name, name_type


def batch_rename(path, name, name_type):
    num = 1
    script = __file__

    # files = os.listdir(path)
    # for file in files:
    #     file_new = name % num
    #     if(path+'/'+file == script):
    #         continue
    #     os.rename(path+'/'+file,path+'/'+file_new)
    #     print("%s改名为%s" % (file,file_new))
    #     num+=1

    print('start----------')
    for root, dirs, files in os.walk(path):
        for file in files:
            file_new = name % (num,)
            if path + '/' + file == script:
                continue
            if file.lower().find(name_type) == -1:
                continue
            os.rename(path + '/' + file, path + '/' + file_new)
            print("\"%s\" 改名为 \"%s\"" % (file, file_new))
            num += 1
    print('end------------')


if __name__ == "__main__":
    while True:
        path, name, name_type = user_input_params()
        batch_rename(path, name, name_type)

        is_continue = input("是否继续? [Y/n]")
        if is_continue == '' or is_continue == 'Y' or is_continue == 'y':
            continue
        else:
            break
