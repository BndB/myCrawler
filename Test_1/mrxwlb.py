__author__ = 'ZRT'
# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import jieba
import jieba.analyse
import urllib
import urllib2
import re
import os
 
class MRXWLB:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = { 'User-Agent' : self.user_agent }
        self.url = 'http://mrxwlb.com/page/'
        self.resultdir = ''
        self.enable = False

    def makedir(self,dirname):
        self.resultdir = os.getcwd() + '\\' + dirname
        if not os.path.exists(self.resultdir):
            os.makedirs(self.resultdir)
            print self.resultdir + u' 创建成功'
            return True
        else:
            print self.resultdir + u' 目录已存在'
            return False

    #将传入的中文字符串分割成词
    def fenCi(self,content):
        word_dict = {}
        fobj = open('fenCiData.txt', 'a+')
        for line in fobj:
            dict_n = line.split(',')
            word_dict[dict_n[0]] = int(dict_n[1])
        for line in content.split('\n'):
            # jieba分词
            tags = jieba.analyse.extract_tags(line.strip())
            for item in tags:
                # 统计数量
                if item not in word_dict:
                    word_dict[item] = 1
                else:
                    word_dict[item] += 1
        for key in word_dict:
            #print key, word_dict[key]
            #tagsw += key + ',' + str(word_dict[key]) + '\n'
            fobj.write(key + ',' + str(word_dict[key]) + '\n')
        fobj.flush()
        fobj.close()

    #传入某一页的索引获得页面代码
    def getPage(self,reqUrl):
        try:
            request = urllib2.Request(reqUrl,headers = self.headers)
            response = urllib2.urlopen(request)
            #将页面转化为UTF-8编码
            pageCode = response.read().decode('utf-8')
            return pageCode
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"网页连接失败,错误原因",e.reason
                return None

    #获取每篇新闻内容
    def getContent(self,url):
        try:
            request = urllib2.Request(url, headers=self.headers)
            response = urllib2.urlopen(request)
            content = response.read().decode('utf-8')
            # 获取标题
            pattern = re.compile('<header class.*?header">.*?<h1.*?title">(.*?)</h1>.*?<time class.*?>(.*?)</time>',
                                 re.S)
            items = re.findall(pattern, content)
            for item in items:
                print item[0].strip() + ' -- ' + item[1].strip()
            '''
            # 获取主要内容
            pattern = re.compile('<div class="title">(.*?)</div>', re.S)
            items = re.findall(pattern, content)
            for item in items:
                print item.strip()
            '''
            # 获取详细全文
            pattern = re.compile('<p><span style.*?">(.*)<!--repaste.body.end-->', re.S)
            items = re.findall(pattern, content)
            detailxw = ''
            for item in items:
                item = re.sub('</?[^>]+>', '', item)
                detailxw = detailxw.join(item)
            return detailxw
        except urllib2.URLError, e:
            if hasattr(e,"reason"):
                print u"网页连接失败,错误原因",e.reason
                return None

    #获取每日新闻连接
    def getPageItems(self,pageIndex):
        pageCode = self.getPage(self.url+str(pageIndex))
        if not pageCode:
            self.enable = False
            print u"页面加载失败，退出...."
            return None
        pattern = re.compile('<h1 class="entry-title">.*?<a href="(.*?)" title="Continue reading(.*?)">',re.S)
        items = re.findall(pattern,pageCode)
        for item in items:
            if item[1].find(u'新闻联播文字版')>=0 and item[1].find('2017')>=0:
                #print item[0].strip() + ' -- ' + item[1].strip()
                fname = self.resultdir+'\\'+item[1].strip() + '.txt'
                fobj = open(fname, 'w')
                xwContent = self.getContent(item[0].strip())
                #fobj.write(item[0]+'\r\n')
                #self.fenCi(xwContent)
                fobj.write(xwContent)
                fobj.close()

    #开始方法
    def start(self):
        self.enable = True
        self.makedir('mrxwlb')
        while self.enable:
            self.getPageItems(self.pageIndex)
            self.pageIndex += 1

spider = MRXWLB()
spider.start()