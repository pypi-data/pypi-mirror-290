import argparse
from easygui import *
import sys
def main():
    # 创建一个 ArgumentParser 对象
    parser = argparse.ArgumentParser(description='paddy命令行工具')

    # 添加 -R 选项
    parser.add_argument('-R', '--option-r', action='store_true', help='这个命令可以运行程序(.p)')

    # 添加 -C 选项
    parser.add_argument('-C', '--option-c', action='store_true', help='这个命令可以编译程序(.p)为可执行程序(.exe)')
    parser.add_argument('-E', '--option-e', action='store_true', help='这个命令搜索错误报告代码的含义以及解决方案')
    # 解析命令行参数
    args = parser.parse_args()

    # 检查是否接收到了 -R 选项
    if args.option_r:
        print('\033[106m\033[30m正在导入GUI模块')

        print('正在新建对话框……')
        filename = enterbox('请输入您的.p文件的名字(请加上后缀)')
        print('正在导入系统模块……')
        import sys
        print('正在检查后缀')
        try:
            if '.p' not in filename and filename!='':
                textbox('错误', '错误', '错误\n\t错误环境：解释\n\t错误原因：输入的文件不是.p文件，paddy解释器无法识别\n\t错误代码：12')
                print('程序退出：程序因编译时遇到错误而退出')
                print('Program Exit: The program exited due to an error encountered during compilation.')
                sys.exit(12)
        except TypeError:
            print('\033[0m___________')
            print('程序因^C而退出')
            sys.exit(0)
        print('正在新建替换文件……')
        file = open('other/modified.txt', 'w')
        print('正在关闭文件……')
        file.close()
        single_line_comments = 0
        multi_line_comment_lines = 0
        in_multi_line_comment = False
        print('正在计算行数……')
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                lines = sum(1 for line in file)
        except:
            textbox('错误','错误','错误环境：解释运行\n错误原因：文件不存在'+filename+'\n错误详细：FileNotFoundError: [Errno 2] No such file or directory: '+filename+'\n错误代码:11')
            print('\033[0m__________')
            print('程序退出：程序因编译时遇到错误而退出')
            print('Program Exit: The program exited due to an error encountered during compilation.')
            sys.exit(11)
        print('正在检查注释……')
        print('打开源文件……')
        with open(filename, 'r', encoding='utf-8') as file:
            for line_number, line in enumerate(file, start=1):
                stripped_line = line.strip()
                # Check for multi-line comment start
                if stripped_line.startswith('"""') or stripped_line.startswith("'''"):
                    # Toggle multi-line comment flag and skip the rest of the line
                    in_multi_line_comment = not in_multi_line_comment
                    # Also count this line as part of the multi-line comment
                    if in_multi_line_comment:
                        multi_line_comment_lines += 1
                    continue

                if in_multi_line_comment:
                    multi_line_comment_lines += 1
                    continue

                    # Check for single-line comment
                if '#' in stripped_line:
                    # If '#' is not part of a string, it's a comment
                    if not (stripped_line.startswith('"') or stripped_line.startswith("'")) or \
                            (stripped_line.count('"') % 2 == 0 and stripped_line.count("'") % 2 == 0):
                        single_line_comments += 1
        try:
            print('正在定义开头项……')
            start_with = '如果'
            print('正在定义被覆盖项……')
            old_char = ' 而且 '
            print('正在定义替换项……')
            new_char = ' and '
            with open(filename, 'r', encoding='utf-8') as infile, open('other/modified.txt', 'w',
                                                                       encoding='utf-8') as outfile:
                for line in infile:
                    if line.startswith(start_with):
                        modified_line = line.replace(old_char, new_char)
                        outfile.write(modified_line)
                    else:
                        outfile.write(line)
        except FileNotFoundError:
            textbox('错误', '错误', '错误\n\t错误环境：解释\n\t错误原因：输入的文件不存在(' + filename + ')')
            sys.exit(1)
        try:
            print('正在打开替换后的文件')
            with open('other/modified.txt', 'r', encoding='utf-8') as outfile:
                print('正在读取文件内容')
                readstr = outfile.read()
        except FileNotFoundError:
            textbox('错误', '错误', '错误\n\t错误环境：解释\n\t错误原因：输入的文件不存在')
            sys.exit(1)
        print('打开解释文件……')
        with open('paddyruntime.py', 'w', encoding='gbk') as file:
            print('写入编码格式……')
            file.write('# -*- coding: gbk -*-\n')
            print('写入导入代码……')
            file.write('from package.paddy import *\n')
            print('写入源文件……')
            file.write(readstr)
            print('导入文件操作模块……')
            import os
            print('导入运行器……')
        import subprocess
        print('导入时间模块……')
        import time
        print('正在记录时间戳……')
        start_time = time.perf_counter()
        print('执行解释后的代码……')
        print("\033[0m=========", filename, "==========")
        subprocess.run(['python', 'paddyruntime.py'])
        print('===========================')
        print('\033[106m\033[30m正在记录时间戳……')
        end_time = time.perf_counter()
        print('正在计算时间……')
        elapsed_time = end_time - start_time
        print('正在转换单位到毫秒……')
        elapsed_time_milliseconds = elapsed_time * 1000
        print('正在转换单位到微秒……')
        elapsed_time_microseconds = elapsed_time * 1_000_000
        print('\033[0m_______________________________')
        print('运行信息及程序信息')
        print('\033[95m\t运行时间:(秒)', elapsed_time)
        print('\t运行时间:(毫秒)', elapsed_time_milliseconds)
        print('\t运行时间:(毫秒)', elapsed_time_microseconds)
        print('\t程序行数:', lines)
        print('\t程序注释行数:(单行注释符#)', single_line_comments)
        print('\t程序注释行数:(多注释符""" """)', multi_line_comment_lines)
        print('\033[0m_______________________________')
        input('运行完毕，按回车退出')
        os.remove('paddyruntime.py')
    if args.option_c:
        import sys
        print("已接收到 -C 选项，这里你可以添加相应的代码。")
        sys.exit(0)

        # 如果没有接收到任何选项，这里也可以添加相应的处理逻辑
    # 注意：由于 -R 和 -C 是可选的，且都是 action='store_true'，
    # 因此如果没有接收到任何选项，程序不会进入上述if语句块。
    # 如果需要处理“没有接收到任何选项”的情况，你可能需要添加一个额外的参数（如 --no-options）
    # 或者检查 args 对象的其他属性来推断
    if args.option_e:
        ec=input('\033[0m错误代码：')
        if ec=='11':
            print('错误概述：错误代码11是指程序在编译的过程中(例如使用-R或-C)无法找到输入的文件。')
            print('错误解决1：新建一个文件')
            print('错误解决2：检查一下有没有输入错文件名')
        elif ec=='12':
            print('错误概述：错误代码12是指程序在编译的过程中(例如使用-R或-C)文件的后缀(不是.p)不对。')
            print('错误解决1：新建一个对的文件(.p)')
            print('错误解决2：检查一下有没有输入错文件的后缀')
    else:
        print('\033[91m[错误]没有参数或参数不正确')
        print('\033[34m[提示]如果不知道命令，可以使用--help或-h查看帮助。')
if __name__ == '__main__':
    main()