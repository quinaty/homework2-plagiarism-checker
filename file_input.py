import os
import argparse

# 从命令行读取文件
def read_file_from_args():
    parser = argparse.ArgumentParser(description='从命令行读取文件')

    #分别读取原始文件、疑似抄袭文件、答案文件的路径
    parser.add_argument('org_file',type=str)
    parser.add_argument('org_add_file',type=str)
    parser.add_argument('answer_file',type=str)

    args = parser.parse_args()
    return [args.org_file, args.org_add_file, args.answer_file]
