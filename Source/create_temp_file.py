# -*- coding: utf-8 -*-
__author__ = '奎'

if __name__ == '__main__':
    with(open("temp.txt", 'w')) as f:
        f.write("hello world.")
        f.close()
