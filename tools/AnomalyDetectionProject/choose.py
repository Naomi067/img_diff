"""
filename: choose.py
author: Xin Wang<wangxin7@corp.netease.com>
created: 2023-06-19
modified: 2023-08-11
description: 用来本地化对比两个版本的时装图片,后续待制作到web上
"""
import os
import subprocess
import tkinter as tk
from tkinter import ttk
import utils

if __name__ == '__main__':
    # 指定文件目录
    dir_path = 'G:/img_diff/tools/AllImages/L32'

    # 获取所有文件夹名称
    dir_list = os.listdir(dir_path)
    dir_list = [d for d in dir_list if os.path.isdir(os.path.join(dir_path, d))]

    # 创建主窗口
    root = tk.Tk()
    root.title("时装对比版本选择")

    # 创建下拉框标签和提示标签
    start_label = ttk.Label(root, text="初始版本")
    start_label.grid(column=0, row=0, padx=10, pady=10)

    start_file_label = ttk.Label(root, text="")
    start_file_label.grid(column=2, row=0, padx=10, pady=10)

    end_label = ttk.Label(root, text="对比版本")
    end_label.grid(column=0, row=1, padx=10, pady=10)

    end_file_label = ttk.Label(root, text="")
    end_file_label.grid(column=2, row=1, padx=10, pady=10)

    # 创建下拉框
    start_var = tk.StringVar()
    start_var.set(dir_list[0])

    start_dropdown = ttk.Combobox(root, textvariable=start_var, values=dir_list)
    start_dropdown.grid(column=1, row=0, padx=10, pady=10)

    end_var = tk.StringVar()
    end_var.set(dir_list[0])

    end_dropdown = ttk.Combobox(root, textvariable=end_var, values=dir_list)
    end_dropdown.grid(column=1, row=1, padx=10, pady=10)

    # # 创建提示标签
    # file_label = ttk.Label(root, text="")
    # file_label.grid(column=0, row=2, columnspan=2)

    # 创建确认按钮
    def confirm():
        # print(start_var.get(), end_var.get())
        # subprocess.run(["python3", "classifybypolicy.py", start_var.get(), end_var.get()])
        # root.destroy()
        cmd = ["python3", "classifybypolicy.py", start_var.get(), end_var.get()]
        # 在后台运行子进程并将输出重定向到文件中
        with open("output.txt", "w") as f:
            subprocess.Popen(cmd, stdout=f, stderr=f)

        root.destroy()

    confirm_button = ttk.Button(root, text="确认", command=confirm)
    confirm_button.grid(column=0, row=2, columnspan=2, padx=10, pady=10)

    # 定义下拉框选择函数
    def combobox_selected_start(event):
        app_list = utils.getVersionIncludes(start_var.get())
        start_file_label.configure(text="".join("包含时装类型:"+str(app_list)))
    
    def combobox_selected_end(event):
        app_list = utils.getVersionIncludes(end_var.get())
        end_file_label.configure(text="".join("包含时装类型:"+str(app_list)))

    start_dropdown.bind("<<ComboboxSelected>>", combobox_selected_start)
    end_dropdown.bind("<<ComboboxSelected>>", combobox_selected_end)

    # 运行主循环
    root.mainloop()