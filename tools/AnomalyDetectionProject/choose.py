"""
filename: choose.py
author: Xin Wang<wangxin7@corp.netease.com>
created: 2023-06-19
modified: 2023-11-06
description: 用来本地化对比两个版本的时装图片本地前端
"""
import subprocess
import tkinter as tk
from tkinter import ttk
import utils
import sys

if __name__ == '__main__':
    # 创建主窗口
    root = tk.Tk()
    root.geometry('600x300')
    root.title("L32时装对比")
    root.iconphoto(True, tk.PhotoImage(file='./template/l32.png'))
    # 将背景颜色设置为白色
    root.configure(background='white')

    # 创建"时装对比模式"按钮
    fashion_button = tk.Button(root, text="时装对比模式", command=lambda: start(utils.Mode.FASHION))
    fashion_button.grid(column=0, row=0, padx=10, pady=10)

    # 创建"家园对比模式"按钮
    home_button = tk.Button(root, text="家园对比模式", command=lambda: start(utils.Mode.HOME))
    home_button.grid(column=2, row=0, padx=10, pady=10)

    # 创建"家园对比模式"按钮
    d21_button = tk.Button(root, text="D21对比模式", command=lambda: start(utils.Mode.D21))
    d21_button.grid(column=4, row=0, padx=10, pady=10)

    def start(mode):
        print(mode)
        # 隐藏模式按钮
        fashion_button.grid_forget()
        home_button.grid_forget()
        d21_button.grid_forget()
        global report_home_mode
        report_home_mode = mode.value
        # 获得选择框数据
        dir_list_ori = utils.getOriVersion(mode)
        dir_list_tar = utils.getAllWeekVersions(mode)
        # 提示标签
        start_label = ttk.Label(root, text="初始版本")
        start_label.grid(column=0, row=0, padx=10, pady=10)
        start_label.configure(background='white')

        start_file_label = ttk.Label(root, text="")
        start_file_label.grid(column=2, row=0, padx=10, pady=10)
        start_file_label.configure(background='white')

        start_time_label = ttk.Label(root, text="")
        start_time_label.grid(column=4, row=0, padx=10, pady=10)
        start_time_label.configure(background='white')

        end_label = ttk.Label(root, text="对比版本")
        end_label.grid(column=0, row=1, padx=10, pady=10)
        end_label.configure(background='white')

        end_file_label = ttk.Label(root, text="")
        end_file_label.grid(column=2, row=1, padx=10, pady=10)
        end_file_label.configure(background='white')

        end_time_label = ttk.Label(root, text="")
        end_time_label.grid(column=4, row=1, padx=10, pady=10)
        end_time_label.configure(background='white')

        # 创建下拉框
        start_var = tk.StringVar()
        start_var.set(dir_list_ori[0])

        start_dropdown = ttk.Combobox(root, textvariable=start_var, values=dir_list_ori)
        start_dropdown.grid(column=1, row=0, padx=10, pady=10)

        end_var = tk.StringVar()
        end_var.set(dir_list_tar[0])

        end_dropdown = ttk.Combobox(root, textvariable=end_var, values=dir_list_tar)
        end_dropdown.grid(column=1, row=1, padx=10, pady=10)

        # 定义下拉框选择函数-显示时装版本额外信息
        def combobox_selected_start(event):
            # print(start_var.get())
            app_list = utils.getVersionFashionInfo(start_var.get())
            school = utils.getSchoolIncludes(start_var.get())
            time = utils.timeFormat(start_var.get())
            start_file_label.configure(text="".join("职业{}外观类型{}".format(school,app_list)))
            start_time_label.configure(text="".join("采样时间:{}".format(time)))
        
        def combobox_selected_end(event):
            app_list = utils.getVersionFashionInfo(end_var.get())
            school = utils.getSchoolIncludes(end_var.get())
            time = utils.timeFormat(end_var.get())
            end_file_label.configure(text="".join("职业{}外观类型{}".format(school,app_list)))
            end_time_label.configure(text="".join("采样时间:{}".format(time)))

        # 定义下拉框选择函数-显示家具版本额外信息
        def combobox_selected_start_home(event):
            time = utils.timeFormat(start_var.get())
            start_time_label.configure(text="".join("采样时间:{}".format(time)))
        
        def combobox_selected_end_home(event):
            time = utils.timeFormat(end_var.get())
            end_time_label.configure(text="".join("采样时间:{}".format(time)))
        
        # 定义下拉框选择函数-显示D21版本额外信息
        def combobox_selected_start_D21(event):
            time = utils.timeFormat(utils.extractTimestamp(start_var.get()))
            start_time_label.configure(text="".join("采样时间:{}".format(time)))
        
        def combobox_selected_end_D21(event):
            time = utils.timeFormat(utils.extractTimestamp(end_var.get()))
            end_time_label.configure(text="".join("采样时间:{}".format(time)))

        if mode == utils.Mode.FASHION:
            start_dropdown.bind("<<ComboboxSelected>>", combobox_selected_start)
            end_dropdown.bind("<<ComboboxSelected>>", combobox_selected_end)
        elif mode == utils.Mode.HOME:
            start_dropdown.bind("<<ComboboxSelected>>", combobox_selected_start_home)
            end_dropdown.bind("<<ComboboxSelected>>", combobox_selected_end_home)
        elif mode == utils.Mode.D21:
            start_dropdown.bind("<<ComboboxSelected>>", combobox_selected_start_D21)
            end_dropdown.bind("<<ComboboxSelected>>", combobox_selected_end_D21)


        # 开始对比函数
        def confirm():
            # 隐藏选择框和开始对比按钮
            start_dropdown.grid_forget()
            start_label.grid_forget() 
            end_label.grid_forget() 
            end_dropdown.grid_forget()
            confirm_button.grid_forget() 
            skip_button.grid_forget()
            start_file_label.grid_forget()
            start_time_label.grid_forget()
            end_file_label.grid_forget()
            end_time_label.grid_forget()

            global waiting_label
            # 创建等待计算完成标签
            waiting_label = ttk.Label(root, text="等待算法比较完成..........")
            waiting_label.grid(column=0, row=2, columnspan=2, padx=10, pady=10)
            waiting_label.configure(background='white')

            # 将按钮设置为全局变量，以便在 reset() 函数中使用
            global continue_button
            global report_button

            # 添加"继续比较"和"选择报告"按钮
            continue_button = ttk.Button(root, text="继续比较", command=reset)
            report_button = ttk.Button(root, text="选择报告", command=lambda: createReport(False))
            #调用比较算法
            cmd = ["python3", "classifybypolicy.py", start_var.get(), end_var.get(), str(report_home_mode)]
            # 显示等待计算完成标签
            waiting_label.grid()
            # 在后台运行子进程并将输出重定向到文件中
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # 等待子进程完成
            stdout, stderr = process.communicate()
            # 输出子进程的输出和错误信息
            print(stdout.decode("utf-8", errors='replace'))
            print(stderr.decode("utf-8", errors='replace'))

            # 输出完成后展示信息
            waiting_label.config(text="{}-{}比较完成~".format(start_var.get(), end_var.get()))
            continue_button.grid(column=0, row=3, padx=10, pady=10)
            report_button.grid(column=1, row=3, padx=10, pady=10)
            root.update()

        # 继续比较函数
        def reset():
            # 显示选择框和开始对比按钮
            start_dropdown.grid(column=1, row=0, padx=10, pady=10)
            start_dropdown.current(0)
            end_dropdown.grid(column=1, row=1, padx=10, pady=10)
            end_dropdown.current(0)
            start_label.grid(column=0, row=0, padx=10, pady=10)
            end_label.grid(column=0, row=1, padx=10, pady=10)
            confirm_button.grid(column=0, row=2,  padx=10, pady=10)
            skip_button.grid(column=2, row=2,  padx=10, pady=10)
            start_file_label.grid(column=2, row=0, padx=10, pady=10)
            start_time_label.grid(column=4, row=0, padx=10, pady=10)
            end_file_label.grid(column=2, row=1, padx=10, pady=10)
            end_time_label.grid(column=4, row=1, padx=10, pady=10)
            
            # 隐藏"继续比较"和"选择报告"按钮
            continue_button.grid_forget()
            report_button.grid_forget()
            waiting_label.grid_forget()
            root.update()

        # 创建开始对比按钮
        confirm_button = ttk.Button(root, text="开始对比", command=confirm)
        confirm_button.grid(column=0, row=2, padx=10, pady=10)

        def createReport(is_skip):
            # 创建报告流程
            def formal_report():
                # 生成正式报告
                formal_report_button.grid_forget()  # 隐藏生成正式报告按钮
                for frame in frames:
                    frame.grid_forget()
                waiting_label = ttk.Label(root, text="正在生成正式报告...............")
                waiting_label.grid(column=0, row=2, columnspan=2, padx=10, pady=10)
                waiting_label.configure(background='white')
                root.update()
                cmd = ["python3", "makereport.py", str(selected_versions), str(count), "0", str(report_home_mode)]
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                waiting_label.grid()
                # 在后台运行子进程并将输出重定向到文件中
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                # 等待子进程完成
                stdout, stderr = process.communicate()
                # 输出子进程的输出和错误信息
                print(stdout.decode("utf-8", errors='replace'))
                print(stderr.decode("utf-8", errors='replace'))
                waiting_label.config(text="正式报告已生成，请查收邮件")
                root.update()

            def confirm_selection():
                # 勾选的结果目录
                global selected_versions, count
                selected_versions = []
                for idx, name in enumerate(name_dirs):
                    if checkbox_vars[idx].get():
                        selected_versions.append(str(name))
                # selected_versions中去重且add和abnormal只保留一个
                unique_strings = []
                seen_numbers = set()
                for string in selected_versions:
                    number = string.split('_')[1]
                    if number not in seen_numbers:
                        unique_strings.append(string)
                        seen_numbers.add(number)
                count = 0
                # 勾选的结果目录对应的比较总数
                for i in unique_strings:
                    if mode == utils.Mode.FASHION:
                        count += utils.getTotalCountByResult(i) 
                    elif mode == utils.Mode.HOME:
                        count += utils.getHomeTotalCountByResult(i)

                # 遍历所有的Frame和生成报告按钮
                for frame in frames:
                    frame.grid_forget()
                create_button.grid_forget()
                waiting_label = ttk.Label(root, text="等待测试报告生成中..........")
                waiting_label.grid(column=0, row=2, columnspan=2, padx=10, pady=10)
                waiting_label.configure(background='white')
                print(selected_versions,str(count))
                print(str(report_home_mode))
                cmd = ["python3", "makereport.py",  str(selected_versions), str(count),"1", str(report_home_mode)]
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                # 显示等待计算完成标签
                waiting_label.grid()
                        # 等待子进程完成
                # 等待子进程完成
                stdout, stderr = process.communicate()
                # 输出子进程的输出和错误信息
                print(stdout.decode("utf-8", errors='replace'))
                print(stderr.decode("utf-8", errors='replace'))
                # while True:
                #     return_code = process.poll()
                #     if return_code is not None:
                #         break
                #     root.update()
                #     # 子进程执行完成后，更新等待标签的文本
                waiting_label.config(text="测试报告已输出！请查收邮件")
                global formal_report_button
                formal_report_button = ttk.Button(root, text="生成正式报告", command=formal_report)
                formal_report_button.grid(column=0, row=3, padx=10, pady=10)
                close_button = ttk.Button(root, text="结束", command=root.destroy)
                close_button.grid(column=1, row=3, columnspan=2, padx=10, pady=10)
                root.update()

            if not is_skip:
                continue_button.grid_forget()
                report_button.grid_forget()
                waiting_label.grid_forget()
            # 创建多选框
            target_dirs,name_dirs,output_dirs = utils.getThisWeekAllReportListbyMode(mode)
            row = 3  # 开始的行号
            col = 0  # 开始的列号
            checkbox_vars = []
            frames = []  # 保存所有的Frame
            if not name_dirs:  # 如果name_dirs为空
                waiting_label.config(text="无当周报告结果，请重新选择比较版本！")
                continue_button.grid(column=0, row=4, padx=10, pady=10)
                report_button.grid_forget()
            else:
                for i in range(0,len(name_dirs)):
                    dir = name_dirs[i]
                    output = output_dirs[i]
                    var = tk.BooleanVar()
                    var.set(False)
                    checkbox_vars.append(var)
                    frame = ttk.Frame(root)
                    frame.grid(column=col, row=row, padx=10, pady=10, sticky="w")
                    label = ttk.Label(frame, text=output)
                    label.pack(side="left")
                    label.configure(background='white')
                    checkbutton = ttk.Checkbutton(frame, text=dir, variable=var, onvalue=True, offvalue=False)
                    checkbutton.pack(side="left")
                    frames.append(frame)  # 将Frame添加到列表中
                    row += 1  # 每次换行
                create_button = ttk.Button(root, text="生成测试报告", command=confirm_selection)
                create_button.grid(column=0, row=row, padx=10, pady=10)
        
        # 跳过对比直接选报告
        def skipToReport():
            # 隐藏选择框和开始对比按钮
            start_dropdown.grid_forget()
            start_label.grid_forget() 
            end_label.grid_forget() 
            end_dropdown.grid_forget()
            confirm_button.grid_forget() 
            start_file_label.grid_forget()
            start_time_label.grid_forget()
            end_file_label.grid_forget()
            end_time_label.grid_forget()
            skip_button.grid_forget()
            createReport(True)

        # 创建开始对比按钮
        skip_button = ttk.Button(root, text="跳过对比", command=skipToReport)
        skip_button.grid(column=1, row=2, padx=10, pady=10)

    # 运行主循环
    root.mainloop()