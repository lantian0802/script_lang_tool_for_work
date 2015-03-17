#-*- coding: UTF-8 -*-
import os
import sys
import codecs

DEFAULT_CODEC = sys.getfilesystemencoding()

def GBK_2_UTF8(src,dst):
    ## with ... as 的用法类似于 try ...except ... finally 的用法，with后面的对象有 __enter__和 __exit__方法，f会是__enter__
    ## 的放回值，当执行完毕后会调用__exit__方法
    with codecs.open(src,"r","gbk") as f:
        content = f.read()
    with codecs.open(dst,"w","utf-8") as f:
        f.write(content)

def main():
    ## join函数的意思是将多个路径拼接在一起，dirname是返回目录，
    ## os.path.abspath(__file__) 返回当前文件的的绝对路径
    ## os.path.dirname 返回当前绝对路径的上一级目录
    ## os.walk 返回 目录下的 顶层目录 root，顶层目录下的 dirs 子目录和 顶层目录下的 files
    for root, dirs, files in os.walk(os.path.join(os.path.dirname(os.path.abspath(__file__)),"src")):
        for name in files:
            GBK_2_UTF8(os.path.join(root, name),os.path.join(root, name))
    print "Convert files finished!"

if __name__ == "__main__":
    main()