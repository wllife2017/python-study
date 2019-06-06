# -*- coding: UTF-8 -*-
import os
import sys
import codecs
def calc_num_of_lines(filename):
    """
    计算python文件的行数
    args:
        filename: 文件名
    returns：行数

    raise:
        AssertError: 参数不合法
        IOError: 读取文件失败
    """
    # 参数有效性检查
    flag = isinstance(filename, str) and \
            os.path.exists(filename) and \
            filename[-3:].lower() == ".py"
    assert flag, u"参数不合法"

    with codecs.open(filename, "r", "utf-8") as f:
        lines = f.readlines()

    lines = [line.lstrip() for line in lines]
    def foo(x):
       return len(x) > 0 and (not x.startswith("#"))
    lines = list(filter(foo, lines))
    count = len(lines)
    return count

def deal_one_dir(dir_path):
    items = os.listdir(dir_path)
    cnt = 0
    for item in items:
        name = os.path.join(dir_path, item)
        if os.path.isdir(name):
            cnt = cnt + deal_one_dir(name)
        elif name[-3:].lower() == ".py":
            cnt = cnt + calc_num_of_lines(name)
    return cnt

filename = "main.py"
c = calc_num_of_lines(filename)
print(c)
