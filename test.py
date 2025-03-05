import unittest
import os
import tempfile
from main import jaccard_similarity, main
from file_processing import file_read, file_write, FileProcessor

class TestTextSimilarity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = tempfile.TemporaryDirectory()
        cls.test_files = {
            'empty.txt': '',
            'chinese.txt': '我爱北京天安门',
            'mixed.txt': 'Hello 你好 123',
            'special_chars.txt': '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~',
        }
        for filename, content in cls.test_files.items():
            path = os.path.join(cls.test_dir.name, filename)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

    @classmethod
    def tearDownClass(cls):
        """清理临时目录"""
        cls.test_dir.cleanup()

    def test_file_read_success(self):
        """测试文件读取成功"""
        path = os.path.join(self.test_dir.name, 'chinese.txt')
        content = file_read(path)
        self.assertEqual(content, self.test_files['chinese.txt'])

    def test_file_read_not_found(self):
        """测试文件不存在异常"""
        with self.assertRaises(FileNotFoundError):
            file_read('non_existent_file.txt')


    def test_text_normalization(self):
        """测试文本规范化处理"""
        fp = FileProcessor([os.path.join(self.test_dir.name, 'mixed.txt')])
        normalized = fp.paths_normalized_pairs.values()
        expected = ['Hello', '你好', '123']
        self.assertEqual(list(normalized)[0], expected)

    def test_ngram_generation_chinese(self):
        """测试中文3-gram生成"""
        fp = FileProcessor([os.path.join(self.test_dir.name, 'chinese.txt')])
        ngrams = fp.paths_ngram_pairs_3.values()
        expected = {
            '我 爱 北', '爱 北 京', '北 京 天',
            '京 天 安', '天 安 门',
        }
        self.assertEqual(set(list(ngrams)[0]), expected, msg='测试中文3-gram生成失败')

    def test_large_file_handling(self):
        """测试大文件处理性能"""
        # 生成1MB测试文件
        large_content = 'a' * 1024 * 1024
        large_path = os.path.join(self.test_dir.name, 'large.txt')
        with open(large_path, 'w') as f:
            f.write(large_content)

        # 测试处理时间
        import time
        start = time.time()
        fp = FileProcessor([large_path])
        processing_time = time.time() - start

        self.assertLess(processing_time, 2)  # 确保2秒内处理完成

    def test_file_read_permission_error(self):
        """测试文件权限异常"""
        if os.name == 'posix':  # 仅Linux/Mac测试
            path = os.path.join(self.test_dir.name, 'no_permission.txt')
            with open(path, 'w') as f:
                f.write('test')
            os.chmod(path, 0o222)  # 只写权限

            with self.assertRaises(PermissionError):
                file_read(path)

    def test_file_write_permission_error(self):
        """测试写入权限异常"""
        if os.name == 'posix':
            path = '/root/protected_file.txt'  # 假设无写入权限
            with self.assertRaises(PermissionError):
                file_write(path, "test data")

    def test_special_char_normalization(self):
        """测试特殊字符处理"""
        fp = FileProcessor([os.path.join(self.test_dir.name, 'special_chars.txt')])
        normalized = list(fp.paths_normalized_pairs.values())[0]
        self.assertEqual(normalized, [])

    def test_empty_file_processing(self):
        """测试空文件处理"""
        fp = FileProcessor([os.path.join(self.test_dir.name, 'empty.txt')])
        ngrams = list(fp.paths_ngram_pairs_3.values())[0]
        self.assertEqual(ngrams, set())

    def test_mixed_language_ngram(self):
        """测试混合语言n-gram生成"""
        fp = FileProcessor([os.path.join(self.test_dir.name, 'mixed.txt')])
        expected = {'Hello 你 好', '你 好 123'}
        test_set = set()
        for value in fp.paths_ngram_pairs_3.values():
            for ngram in value:
                test_set.add(ngram)
        self.assertEqual(test_set, expected)

    def test_commandline_args_missing(self):
        """测试缺少命令行参数"""
        from unittest.mock import patch
        with patch('sys.argv', ['main.py']):
            with self.assertRaises(SystemExit):
                main()

    def test_invalid_file_paths(self):
        """测试无效文件路径"""
        with tempfile.NamedTemporaryFile() as ans_file:
            with self.assertRaises(FileNotFoundError):
                processor = FileProcessor([
                    'invalid_path.txt',
                    'another_invalid.txt',
                    ans_file.name
                ])

    def test_unicode_decode_error(self):
        """测试编码异常处理"""
        # 创建GBK编码文件
        path = os.path.join(self.test_dir.name, 'gbk.txt')
        with open(path, 'w', encoding='gbk') as f:
            f.write('你好')

        # 尝试用默认utf-8读取
        content = file_read(path)
        self.assertIsNone(content)

    def test_single_character_input(self):
        """测试单字符输入"""
        test_path = os.path.join(self.test_dir.name, 'single.txt')
        with open(test_path, 'w') as f:
            f.write('a')

        fp = FileProcessor([test_path])
        self.assertEqual(fp.paths_ngram_pairs[test_path], set())


if __name__ == '__main__':
    unittest.main(verbosity=2)