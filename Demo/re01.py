# -*- coding: utf-8 -*-
__author__ = '奎'

import re
# step1 正则表达式
reg_jpg = r'data-src="(.*?\.jpg)"'
reg_gif = r'data-src="(.*?\.gif)"'
# step2 编译正则表达式为Pattern对象  flags可为多个,使用|分割
# flag类型如下:
# re.I(全拼：IGNORECASE): 忽略大小写（括号内是完整写法，下同）
# re.M(全拼：MULTILINE): 多行模式，改变'^'和'$'的行为（参见上图）
# re.S(全拼：DOTALL): 点任意匹配模式，改变'.'的行为
# re.L(全拼：LOCALE): 使预定字符类 \w \W \b \B \s \S 取决于当前区域设定
# re.U(全拼：UNICODE): 使预定字符类 \w \W \b \B \s \S \d \D 取决于unicode定义的字符属性
# re.X(全拼：VERBOSE): 详细模式。这个模式下正则表达式可以是多行，忽略空白字符，并可以加入注释。
pattern_jpg = re.compile(reg_jpg)
pattern_gif = re.compile(reg_gif)
# 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None

# match(string[, pos[, endpos]])
# 这个方法将从string的pos下标处起尝试匹配pattern；
# 如果pattern结束时仍可匹配，则返回一个Match对象；
# 如果匹配过程中pattern无法匹配，或者匹配未结束就已到达endpos，则返回None。
# pos和endpos的默认值分别为0和len(string)；
# re.match()无法指定这两个参数，参数flags用于编译pattern时指定匹配模式。
# 注意：这个方法并不是完全匹配。
# 当pattern结束时若string还有剩余字符，仍然视为成功。
# 想要完全匹配，可以在表达式末尾加上边界匹配符'$'。
match_jpg = pattern_jpg.match('此处应该有HTML')
match_gif = pattern_gif.match('此处应该有HTML')
# search(string[, pos[, endpos]])
# 这个方法用于查找字符串中可以匹配成功的子串。
# 从string的pos下标处起尝试匹配pattern，
# 如果pattern结束时仍可匹配，则返回一个Match对象；
# 若无法匹配，则将pos加1后重新尝试匹配；
# 直到pos=endpos时仍无法匹配则返回None。
# pos和endpos的默认值分别为0和len(string))；
# re.search()无法指定这两个参数，参数flags用于编译pattern时指定匹配模式。
# 那么它和match有什么区别呢？
# match()函数只检测re是不是在string的开始位置匹配，
# search()会扫描整个string查找匹配，
search_jpg = pattern_jpg.search('此处应该有HTML')
search_gif = pattern_gif.search('此处应该有HTML')
# split(string[, maxsplit])
# 按照能够匹配的子串将string分割后返回列表。
# maxsplit用于指定最大分割次数，不指定将全部分割。
split_jpg = pattern_jpg.split('此处应该有HTML')
split_gif = pattern_gif.split('此处应该有HTML')
# findall
# findall(string[, pos[, endpos]]) | re.findall(pattern, string[, flags]):
# 搜索string，以列表形式返回全部能匹配的子串。
findall_jpg = pattern_jpg.findall('此处应该有HTML')
findall_gif = pattern_gif.findall('此处应该有HTML')
# finditer
# finditer(string[, pos[, endpos]]) | re.finditer(pattern, string[, flags]):
# 搜索string，返回一个顺序访问每一个匹配结果（Match对象）的迭代器。
finditer_jpg = pattern_jpg.finditer('此处应该有HTML')
finditer_gif = pattern_gif.finditer('此处应该有HTML')
# sub
# sub(repl, string[, count]) | re.sub(pattern, repl, string[, count]):
# 使用repl替换string中每一个匹配的子串后返回替换后的字符串。
# 当repl是一个字符串时，可以使用\id或\g<id>、\g<name>引用分组，但不能使用编号0。
# 当repl是一个方法时，这个方法应当只接受一个参数（Match对象），并返回一个字符串用于替换（返回的字符串中不能再引用分组）。
# count用于指定最多替换次数，不指定时全部替换。
def funa(m):
    return m.group(1).title() + ' ' + m.group(2).title()


sub_jpg = pattern_jpg.sub(funa, '此处应该有HTML')
sub_gif = pattern_gif.sub(funa, '此处应该有HTML')
# subn
# subn(repl, string[, count]) |re.sub(pattern, repl, string[, count]):
# 返回 (sub(repl, string[, count]), 替换次数)。
def funb(m):
    return m.group(1).title() + ' ' + m.group(2).title()


subn_jpg = pattern_jpg.sub(funb, '此处应该有HTML')
subn_gif = pattern_gif.sub(funb, '此处应该有HTML')
