#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import os
# sys.path.append('..')
import markdown
import importlib
# importlib.reload(sys)
import shutil

SITE = 'http://blog.binkery.com/'
# ARTICLE_DIR = '../article/'
# HTML_DIR = '../public/'
# print(os.getcwd())
# print(os.path.split(os.path.realpath(__file__))[0])
WORK_PATH = os.path.split(os.path.realpath(__file__))[0]
ARTICLE_DIR = WORK_PATH + '/../article/'
HTML_DIR = WORK_PATH + '/../public/'

print(ARTICLE_DIR)
print(HTML_DIR)

class Article(object):

    def __init__(self, content, title, tag, category, localPath):
        self.content = content
        self.title = title.strip()
        self.tag = []
        for t in tag:
            if t != '':
                self.tag.append(t.strip())
        self.category = []
        for c in category:
            if c != '':
                self.category.append(c.strip())

        fileName = localPath[0:localPath.find('-')]

        self.localFileName = fileName + ".html"
        print("fileName = " + fileName)
        self.link = SITE + 'article/' + fileName + ".html"
        print("link = " + self.link)
        self.date = localPath[0:8]
        print("date = " + self.date)

    def getCategories(self):
        html = ''
        for c in self.category :
            html += '<a href="%scategory/%s/index.html">%s</a>\n' % (SITE, c, c)
        return html

    def getTags(self):
        html = ''
        for t in self.tag :
            html += '<a href="%stag/%s/index.html">%s</a>\n' % (SITE,t,t)
        return html

    def getArticleHeader(self):
        html = '''
            <div class="article_item">
                <h2>
                    <a href="%s">%s</a>
                </h2>
                <div class="line">
                    <span>时间：</span>
                    <span>%s</span>
                </div>
                <div class="line">
                    <span>分类：</span>
                    <span>%s</span>
                </div>
                <div class="line">
                    <span>关键词：</span>
                    <span>%s</span>
                </div>
            </div>
        ''' % (self.link,self.title,self.date,self.getCategories(),self.getTags())
        return html

    def getArticleHeaderAtPage(self):
        html = '''
            <div class="article_header">
                <h1>
                    <a href="%s">%s</a>
                </h1>
                <div class="line">
                    <span>时间：<span>
                    <span>%s</span>
                </div>
                <div>
                    <span>分类：</span>
                    <span>%s<span>
                </div>
                <div>
                    <span>关键词：</span>
                    <span>%s</span>
                </div>
            </div>
        ''' % (self.link,self.title,self.date,self.getCategories(),self.getTags())
        return html

class Site(object):

    def __init__(self):
        self.articles = []
        self.tags = {}
        self.categories = {}

    def addArticle(self,article):
        self.articles.append(article)
        for t in article.tag :
            if t not in self.tags :
                self.tags[t] = []
            self.tags[t].append(article)

        for c in article.category:
            if c not in self.categories :
                self.categories[c] = []
            self.categories[c].append(article)

    def readHtmlTemp(self):
        f = open(WORK_PATH + '/templete/article.html')
        content = f.read()
        f.close()
        return content

    def generate(self):

        self.toHomeIndexPage()
        self.toCategoryHomeIndexPage()
        self.toTagHomeIndexPage()

        for article in self.articles:
            self.toArticlePage(article)

        for tag in self.tags:
            self.toTagPage(tag)

        for c in self.categories:
            self.toCategoryPage(c)

    def toHomeIndexPage(self):
        html = '<div class="">'
        for article in self.articles :
            html += article.getArticleHeader()
        html += '</div>'
        self.writeHtml(html, "首页", 'index.html')

    def toTagHomeIndexPage(self):
        html = ''
        for tag in self.tags.keys() :
            html += '<li><a href="%stag/%s/index.html">%s</a></li>\n' % (SITE,tag,tag)
        self.writeHtml(html,"Tags Home Index Page","tag/index.html")

    def toTagPage(self,tag):
        html = '<div class="">'
        for article in self.tags[tag] :
            html += article.getArticleHeader()
        html += '</div>'
        self.writeHtml(html,tag,"tag/" + tag + "/index.html")

    def toCategoryHomeIndexPage(self):
        html = ''
        for c in self.categories :
            html += '<li><a href="%scategories/%s/index.html">%s</a></li>' % (SITE,c,c)
        self.writeHtml(html,"Category Home Index Page","category/index.html")

    def toCategoryPage(self,category):
        html = '<div class="">'
        for article in self.categories[category] :
            html += article.getArticleHeader()
        html += '</div>'
        self.writeHtml(html,"Category" + category,"category/" + category + "/index.html")

    def toArticlePage(self,article):
        body = markdown.markdown(article.content)
        html = '''
            <div>
                %s
                <div class="">
                %s
                </div>
            </div>
        ''' % (article.getArticleHeaderAtPage(),body)
        self.writeHtml(html,article.title,"article/" + article.localFileName)


    def getCategoryHTML(self):
        html = '\n'
        for c in self.categories :
            html += '<li><a href="%scategory/%s/">%s</a></li>\n' % (SITE, c, c)
        return html

    def writeHtml(self, body, title, filepath):
        html = self.readHtmlTemp()
        html = html.replace('{{article}}', body)
        html = html.replace('{{title}}', article.title)
        html = html.replace('{{categories}}', self.getCategoryHTML())
        print("filepath = " + filepath)
        dir = os.path.dirname(HTML_DIR + filepath)
        print("dir = " + dir)
        if not os.path.exists(dir):
            os.makedirs(dir)
            print("mkdir " + dir)

        fo = open(HTML_DIR + filepath, 'w')
        fo.write(html)
        fo.close()

def generateArticle(path):
    f = open(path,'r')
    content = f.read()
    lines = content.splitlines(True)
    isContentStart = False
    articleTitle = ''
    articleContent = ''
    articleTag = ''
    articleCategory = ''
    articleLocalPath = path[len(ARTICLE_DIR):]
    for line in lines:
        if isContentStart :
            articleContent = articleContent + line
            continue
        elif line.startswith('title') :
            articleTitle = line[6:].strip()
        elif line.startswith('tag') :
            articleTag = line[4:].strip().split(',')
        elif line.startswith('category'):
            articleCategory = line[9:].strip().split(',')
        elif line.find('-----') != -1 :
            isContentStart = True

    f.close()
    return Article(articleContent, articleTitle, articleTag, articleCategory, articleLocalPath)

def deleteDirs(path):
    if not os.path.exists(path) :
        return
    if  os.path.isdir(path):
        for item in os.listdir(path):
            deleteDirs(os.path.join(path, item))
        if not os.listdir(path):
               os.rmdir(path)
    else:
        os.remove(path)

deleteDirs(HTML_DIR)
os.mkdir(HTML_DIR)
os.mkdir(HTML_DIR + "article/")
os.mkdir(HTML_DIR + "tag/")
os.mkdir(HTML_DIR + "style/")

shutil.copy2(WORK_PATH + '/style/style.css', WORK_PATH + '/../public/style/style.css')

files = os.listdir(ARTICLE_DIR)
site = Site()
for file in files:
    print("file = " + file)
    if file == '.git' :
        continue
    path = os.path.join('%s%s' % (ARTICLE_DIR,file))

    article = generateArticle(path)
    site.addArticle(article)

site.generate()
print ('=======')