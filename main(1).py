# -*- coding: UTF-8 -*-
import os
import sys
import codecs
# import re

def calc_num_of_lines(filename):

    """ 计算python文件的行数
    args:
        filename: 文件名
    returns：行数'''

    raise:
        AssertError: 参数不合法
        IOError: 读取文件失败
    """
    # 参数有效性检查
    flag = isinstance(filename, str) and \
            os.path.exists(filename) and \
            filename[-3:].lower() == ".py"
    assert flag, u"参数不合法"

    '''
    这里是普通的注释，
    不是docstring注释
    '''
    with codecs.open(filename, "r", "utf-8") as f:
        lines = f.readlines()

    # 其实用正则表达式更加合适。
    # pattern = r"""def\s+.*:\s+(\'{3}[\s\S]*?\'{3})"""
    # pattern = r"""def\s+.*:\s+(\"{3}[\s\S]*?\"{3})"""
    # for item in re.findall(pattern, ''.join(lines)):
    #     print(item)

    lines = [line.lstrip() for line in lines]
    lines = list(filter(lambda x: len(x) > 0 and (not x.startswith("#")), lines))
    # 去除 docstring注释
    sum = 0
    for index, line in enumerate(lines):
        if line.startswith("def "):
            start_index = None
            for i, s in enumerate(lines[index + 1:]):
                if start_index is None:
                    if s.startswith("'''") or s.startswith('''"""'''):
                        start_index = i
                        start_prefix = s[:3]
                        # 假设换行回车是\r\n, 如果为true说明该注释有多行
                        if start_prefix == s[:-2]:
                            continue
                    else:
                        break
                if start_index is not None and s.endswith(start_prefix + "\r\n"):
                    # 打印docstring注释
                    # for ss in lines[index + 1 + start_index:index + 1 + i + 1]:
                    #     print(ss, end='')
                    sum += i + 1 - start_index
                    break

    count = len(lines) - sum
    return count

def calc_one_dir(root_path):
    '''
    计算一个目录下所有python文件去除空白行和单行注释后的行数总和
    args:
        root_path: 路径
    returns：行数

    raise:
        AssertError: 参数不合法
        IOError: 读取文件失败
    '''
    assert isinstance(root_path, str) and os.path.exists(root_path), "参数不合法"
    items = os.listdir(root_path)
    count = 0
    for item in items:
        name = os.path.join(root_path, item)
        if os.path.isdir(name):
            count += calc_one_dir(name)
        elif name[-3:].lower() == ".py":
            count += calc_num_of_lines(name)
    return count

if __name__ == "__main__":
    filename = sys.argv[0]
    num = calc_num_of_lines(filename)
    print("当前文件是：", filename)
    print("去除空白行、单行注释以及docstring注释后的行数是", num)
    # 查看两个函数的去除空行前的docstring注释
    #print(calc_num_of_lines.__doc__)
    #print(calc_one_dir.__doc__)
