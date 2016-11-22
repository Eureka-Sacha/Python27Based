# -*- coding: utf-8 -*-
# python 2.7.9

__author__ = '奎'
import os
import socket
import urllib
import time
import random
import urllib2
import re


class BaiduImg_Spider:
    """百度图片搜索下载爬虫"""
    def __init__(self):
        """构造函数,初始化基本参数.如搜索关键词,页数,header等..
        --v0.1  单线程无代理下载
        --v1.0  单线程多IP代理下载*
        --v2.0  多线程多IP代理下载*
        """
        self.baiduimg_spider = '百度图片下载爬虫v0.1'
        self.now_page = 1  # 当前页面
        self.min_page = 1  # 开始页面
        self.max_page = 11  # 总共查询页数
        self.empty_page = 0  # 查询不到内容的页面  大于3就停止爬虫
        self.imgs = []  # 需要下载的图片
        self.min_size = 150 * 1024  # 文件最小大小150k
        self.url = 'http://image.baidu.com/search/flip'  # 百度图片搜索URL
        self.word = '新垣结衣'  # 搜索关键词(默认是我老婆)
        self.width = 1920  # 图片长度
        self.height = 1080  # 图片高度
        self.headers = {  # header
                          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                          'Accept-Language': 'zh-CN,zh;q=0.8',
                          # 'Accept-Encoding': 'gzip, deflate, sdch',
                          'Referer': 'http://image.baidu.com/search/flip',
                          'Cookie': 'BDqhfp=%E6%96%B0%E5%9E%A3%E7%BB%93%E8%A1%A3%2B1920x1080%26%260-10-1undefined%26%260%26%261; BAIDUID=CE199AC1B0DC673D5BB2C147C49FD279:FG=1; PSTM=1472647733; BIDUPSID=AB9E31BFF15379B40D2F3E260F795519; MCITY=-236%3A; BDUSS=VBbC16eUUtMURpaWQxZFNjak1nUTU0QWkzV0J1LXhRdVJHT09MVDlWWlNsaTVZSVFBQUFBJCQAAAAAAAAAAAEAAACPTAwqRXVyZWthX1NhY2hhAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFIJB1hSCQdYYz; H_PS_PSSID=1456_18241_17949_21084_17001_21455_21395_21377_21191_21339; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; firstShowTip=1; indexPageSugList=%5B%22%E6%96%B0%E5%9E%A3%E7%BB%93%E8%A1%A3%201920x1080%22%2C%22%E6%96%B0%E5%9E%A3%E7%BB%93%E8%A1%A31080%22%2C%22%E6%96%B0%E5%9E%A3%E7%BB%93%E8%A1%A3%22%5D; cleanHistoryStatus=0; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm;',
                          }
        self.data = {
            'tn': 'baiduimage',
            'ie': 'utf-8',
            'word': self.word + ' ' + str(self.width) + 'x' + str(self.height),
            'pn': '0',
            'gsm': '0',
        }
        self.enable = False  # 是否开启爬虫
        self.dirname = 'D:/FTPService/Admin/'  # 存放目录
        self.erroimgs = []
        socket.setdefaulttimeout(5.0)

    def __setInit(self):
        """私有函数:设置搜索关键词"""
        print '-------%s启动------' % self.baiduimg_spider
        print '请输入搜索关键词与分辨率,用|分割(例:\'新垣结衣|1920|1080\'):'
        while True:
            try:
                temp = str(raw_input())
                if temp is not None and temp != '':
                    temp = temp.split('|')
                    if temp[0] is not None and temp[0] != '':
                        self.word = temp[0]
                    if temp[1] is not None and temp[1] != '':
                        self.width = int(temp[1])
                    if temp[2] is not None and temp[2] != '':
                        self.height = int(temp[2])
                break
            except Exception, e:
                print '参数输入错误请重新输入:'
                continue
        print '搜索关键词: %s ,分辨率: %d x %d' % (self.word, self.width, self.height)
        while True:
            try:
                print '输入回车开始下载图片,或输入"q"退出爬虫...'
                temp = str(raw_input())
                if temp is not None and temp != '' and temp.index('q') > -1:
                    self.enable = False
                else:
                    self.enable = True
                break
            except Exception, e:
                print '###', e.message
                continue
        # 组装header里的referer防止被拦截
        self.data['word'] = self.word + ' ' + str(self.width) + 'x' + str(self.height)
        self.data['pn'] = '0'
        self.headers['Referer'] = self.url + '?' + urllib.urlencode(self.data)
        self.dirname = unicode((self.dirname + self.word + '/'), 'utf-8')
        if not os.path.exists(self.dirname):
            os.mkdir(self.dirname)

    def __getPage(self):
        """页面分析函数"""
        if self.enable and self.empty_page <= 3:
            while self.now_page < self.max_page:
                for i in range(self.now_page, self.max_page):
                    print '>>>>开始获取第%d页的图片' % i
                    self.data['pn'] = str((i - 1) * 20)
                    self.headers['Referer'] = self.url + '?' + urllib.urlencode(self.data)
                    req = urllib2.Request(self.url + '?' + urllib.urlencode(self.data), headers=self.headers)
                    Response = urllib2.urlopen(req)
                    Page = Response.read()
                    unicodePage = Page.decode("UTF-8")
                    imgurllist = re.findall(
                        '"objURL":"(http://[^\{|^\}|^:]*\.[(jpg)?|(jpeg)?|(png)?|(tiff)?|(bmp)?|(gif)?]+)*?"',
                        unicodePage,
                        re.S)
                    for imgurl in imgurllist:
                        headers = {  # header
                                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
                                     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                                     'Accept-Language': 'zh-CN,zh;q=0.8',
                                     }
                        try:
                            connection = urllib2.build_opener().open(urllib2.Request(imgurl, headers=headers))
                        except Exception, e:
                            print '###', e
                            print '###', imgurl
                            print '###', self.headers
                            self.erroimgs.append('Erro=' + str(e) + ',ImgURL=' + str(imgurl))
                            continue
                        try:
                            if int(connection.headers.dict['content-length']) < self.min_size or os.path.exists(
                                            self.dirname + imgurl.split('/')[-1]):
                                continue
                        except Exception, e:
                            print '###', e
                            continue
                        self.imgs.append(imgurl)
                    if self.imgs.__len__() == 0:
                        self.empty_page += 1
                    else:
                        self.__downloadImg()
                    self.now_page = i
                    time.sleep(random.random() * 10)  # 随机延迟 防止被T
                print '已下载完成%d-%d页内容,如需继续请输入"c":' % (self.min_page, self.max_page - 1)
                temp = str(raw_input())
                if temp.lower() == 'c':
                    self.now_page = self.max_page
                    self.min_page = self.max_page
                    self.max_page += 10
                else:
                    self.now_page = self.max_page
            print '图片下载已结束,请到目录 "%s" 下查看图片' % self.dirname.encode('utf-8')
            print '以下为下载失败图片:'
            for erroimg in self.erroimgs:
                print erroimg
        print '-------%s结束------' % self.baiduimg_spider


    def __downloadimg(self):
        """图片下载函数"""
        print '>>开始下载图片(共%d张)' % self.imgs.__len__()
        for img in self.imgs:
            temp = re.split(r'/', img)
            filename = temp[-1]  # 文件名
            try:

                if not os.path.exists(self.dirname + filename):
                    urllib.urlretrieve(img, self.dirname + filename)  # 按照url进行下载，并以其文件名存储到本地目录
                    print '>>', filename, '下载完成'
                else:
                    print '>>', filename, '已存在'
                    continue
            except Exception, e:
                print '###%s' % e
                self.erroimgs.append('错误信息=' + str(e) + '  图片URL=' + str(img))
                continue
        self.imgs = []

    def startModel(self):
        """爬虫入口函数"""
        self.__setInit()
        self.__getPage()

# 开启爬虫
Spider = BaiduImg_Spider()
Spider.startModel()
