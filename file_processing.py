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

# 写入文件内容
def file_write(file_path, data):

    try:
        with open(file_path, 'a+', encoding='utf-8') as file:
                file.write(data)
    except FileNotFoundError:
        print(f"错误：文件 '{file_path}' 不存在")
    except IsADirectoryError:
        print(f"错误：'{file_path}' 是一个目录")
    except PermissionError:
        print(f"错误：没有权限写入 '{file_path}'")
    except UnicodeDecodeError:
        print("错误：文件编码不支持，请尝试指定其他编码方式")
    except Exception as e:
        print(f"写入文件时发生未知错误：{str(e)}")


#初步清洗数据
def file_normalize(data):
    # 去除非中文、英文、数字和空格
    normalized_data = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s]', '', data)
    # 去除多余空格
    normalized_data = re.sub(r'\s+','', normalized_data)
    return split_chinese_english_number(normalized_data.strip().split())

# 切分中文、英文、数字
def split_chinese_english_number(sub_normalized_text):
    result = []
    for text in sub_normalized_text:
        sub_result = re.findall(r'[\u4e00-\u9fa5]+|[a-zA-Z]+|[0-9]+', text)
        result.extend(sub_result)
    return result


# 判断是否为纯中文
def is_chinese(word):
    __is_chinese = True
    for char in word:
        if '\u4e00' > char or char > '\u9fa5':
            __is_chinese = False
            break
    return __is_chinese

# 判断是否为纯英文
def is_english(word):
    __is_english = True
    for char in word:
        if ('a' > char or char > 'z') or ('A' > char or char > 'Z'):
            __is_english = False
            break
    return __is_english

#将中文分割成字，英文、数字不分割
def text_split(normalized_text):
    split_text = []
    for word in normalized_text:
        if is_chinese(word):
            for char in word:
                split_text.append(char)
        else :
            split_text.append(word)

    return split_text


# 生成n-gram
def generate_ngram(phase, n):
    ngram_list = set()
    phase = text_split(phase)
    #print(phase)
    for i in range(len(phase) - n + 1):
        ngram_list.add(' '.join(phase[i:i+n]))
    return ngram_list



class FileProcessor:
    def __init__(self, file_paths):
        self.file_paths = file_paths
        self.paths_contents_pairs = {}
        self.paths_normalized_pairs = {}
        self.paths_ngram_pairs_2 = {}
        self.paths_ngram_pairs_3 = {}

        for path in self.file_paths[0:2]:
            self.paths_contents_pairs[path] = file_read(path)
            self.paths_normalized_pairs[path] = file_normalize(self.paths_contents_pairs[path])
            self.paths_ngram_pairs_2[path] = generate_ngram(self.paths_normalized_pairs[path], 2)
            self.paths_ngram_pairs_3[path] = generate_ngram(self.paths_normalized_pairs[path], 3)

if __name__ == '__main__':
    org_file, org_add_file, answer_file = fi.read_file_from_args()
    file_processor = FileProcessor([org_file, org_add_file, answer_file])
    for content in file_processor.paths_contents_pairs.values():
        print(content,end='\n\n')

    for normalized_text in file_processor.paths_normalized_pairs.values():
        print(normalized_text,end='\n\n')

    for ngram in file_processor.paths_ngram_pairs.values():
        print(ngram,end='\n\n')