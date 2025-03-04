import re
import file_input as fi

# 读取文件内容
def file_read(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"错误：文件 '{file_path}' 不存在")
    except IsADirectoryError:
        print(f"错误：'{file_path}' 是一个目录")
    except PermissionError:
        print(f"错误：没有权限读取 '{file_path}'")
    except UnicodeDecodeError:
        print("错误：文件编码不支持，请尝试指定其他编码方式")
    except Exception as e:
        print(f"读取文件时发生未知错误：{str(e)}")

    return None

class FileProcessor:
    def __init__(self, file_paths):
        self.file_paths = file_paths
        self.paths_contents_pairs = {}
        self.paths_normalized_pairs = {}
        self.paths_ngram_pairs = {}
        self.paths_ngram_pairs = {}

        for path in self.file_paths[0:2] :
            self.paths_contents_pairs[path] = file_read(path)