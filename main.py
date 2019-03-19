#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import codecs
import datetime
import markdown
import time
import config
import template

def write(path,content):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
    with codecs.open(path, "w", "utf-8") as f:
        f.write(content)
        f.close()

def read_path_as_content(path):
    if os.path.isdir(path):
        md_file = os.path.join(path,'index.md')
        if not os.path.exists(md_file):
            return '# no title \n - no keyword \n - no datetime\n'
    else :
        md_file = path
    with open(md_file,'r') as f:
        content = f.read()
    return content

def path_to_html_path(path):
    #print('path_to_html_path ' + path)
    output = ''
    if path == config.site['input'] :
        output = config.site['output'] + 'index.html'    
    elif os.path.isdir(path):
        output =  config.site['output']  + path[len(config.site['input']):] + '/index.html'
    else:
        output =  config.site['output'] + path[len(config.site['input']):-2] + 'html'
    #print(output)
    return output

# 相对路径
def path_to_link(path):
    #print('===== ' + path)
    output = ''
    if path == config.site['input']:
       output = '/index.html'
    if os.path.isdir(path):
        output = '/' + path[len(config.site['input']):] + '/index.html'
    else:
        output = '/' + path[len(config.site['input']):-2] + 'html'
    #print('link = ' + output)
    return output

def write_article_to_file(article,content,path):
    #print(article['link'])
    #print(path)
    #print(content)
    article_content = markdown.markdown(content)
    local_path = path_to_html_path(path)
    article['description'] = ''
    article['content'] = article_content
    #print(local_path)
    result = template.html.format(article=article,site=config.site)
    #print(local_path)
    write(local_path,result)

def read_path_as_article(path):
    if os.path.isdir(path):
        md_file = os.path.join(path,'index.md')
        if not os.path.exists(md_file):
            return {
                'title':'notitle',
                'keyword':'nokeyword',
                'datetime':'nodatetime',
                'link':path_to_link(path)
            }
    else:
        md_file = path
    with open(md_file,'r') as f:
        _title = f.readline().strip().lstrip('#')
        _keyword = f.readline().strip().lstrip('-')
        _datetime = f.readline().strip().lstrip('-')
    return {
        'title':_title,
        'keyword':_keyword,
        'datetime':_datetime,
        'link':path_to_link(path)
    }

def dispatch_path(path):
    article = read_path_as_article(path)
    article_content = read_path_as_content(path)
    if os.path.isdir(path):
        files = os.listdir(path)
        article_content += '\n## 文章列表 \n'
        #print(' ------ article list')
        for f in files:
            if f == 'index.md':
                continue
            child_file = os.path.join(path,f)
            child = read_path_as_article(child_file)
            #print(' --------======== ')
            article_content += '- [' + child['title'] + '](' + child['link'] + ')\n'
    write_article_to_file(article,article_content,path)

    if os.path.isdir(path):
        files = os.listdir(path)
        for f in files :
            #print('=========' +f)
            if f == 'index.md':
                #print('continue')
                continue
            # 最后需要递归一下
            dispatch_path(os.path.join(path,f))

dispatch_path(config.site['input'])
