#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import codecs
import datetime
import markdown
import time


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
    if path == '../content/':
        return '../html/index.html'
    if os.path.isdir(path):
        return '../html' + path[10:] + '/index.html'
    else:
        return '../html' + path[10:-2] + 'html'


def write_article_to_file(article,content,path):
    #print(article['link'])
    #print(path)
    #print(content)
    article_content = markdown.markdown(content)
    local_path = path_to_html_path(path)
    article['description'] = ''
    article['content'] = article_content
    #print(local_path)
    template = '''
    <!DOCTYPE html>
<html lang="zh-cn">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" />
    <meta name="renderer" content="webkit">
    <meta http-equiv="Cache-Control" content="no-siteapp" />
    <meta name ="viewport" content ="initial-scale=1, maximum-scale=1, minimum-scale=1, user-scalable=no">
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
    <meta name="theme-color" content="#337ab7">
    <title>{article[title]} :: {site[app_name]}</title>
    <meta name="keywords" content="{article[keyword]}">
    <meta name="description" content="{article[description]}">
    <link rel="stylesheet" href="{site[app_link]}/style.css">
    <script>
    var _hmt = _hmt || [];
        (function() {{
          var hm = document.createElement("script");
          hm.src = "https://hm.baidu.com/hm.js?1258cd282e3e864279d9edd53837183b";
          var s = document.getElementsByTagName("script")[0]; 
          s.parentNode.insertBefore(hm, s);
        }})();
    </script>
</head>
<body>
<header><p><a href="{site[app_link]}/">记录思考</a></p>
</header>
<nav>
	<ul>
		<li><a href="{site[app_link]}/">首页</a></li>
		<li><a href="{site[app_link]}/daily/">每日思考</a></li>
		<li><a href="{site[app_link]}/blogs/">站点日志</a></li>
	</ul>
</nav>

<div id="div_article">
     <article>
     {article[content]}
     <P> - EOF - </P>
     <p> 本文链接 <a href="{site[app_link]}{article[link]}"> {site[app_link]}{article[link]}</a>，欢迎转载，转载请注明出处。</p>
    </article>
</div>

<footer>
     <p>
        网站更新时间:{site[last_modify_time]}
         网站已经运行<span class=""> {site[since_setup]} </span>天 ,
         离域名到期 {site[to_domain]}天，
         离空间到期 {site[to_space]} 天，</p>
     <p>CopyRight &copy; <a href="{site[app_link]}/">SpacePage.Top</a></p>
</footer>
</body>
</html>
'''.format(article=article,site=site)
    #print(local_path)
    write(local_path,template)

def path_to_link(path):
    #print('===== ' + path)
    if path == '../content/':
       #print('=======')
       return '/index.html'
    if os.path.isdir(path):
        return path[10:] + '/index.html'
    else:
        return path[10:-2] + 'html'

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

def date_from(y,m,d):
    d1 = datetime.date.today()
    d2 = datetime.date(y,m,d)
    return (d1-d2).days

def date_to(y,m,d):
    d1 = datetime.date.today()
    d2 = datetime.date(y,m,d)
    return (d2-d1).days

site = {}
cst_tz = datetime.timezone(datetime.timedelta(hours=8))
site['last_modify_time'] = datetime.datetime.now(tz=cst_tz).strftime("%Y-%m-%d %H:%M:%S")
site['since_setup'] = date_from(2019,1,24)
site['to_domain'] = date_to(2028,6,8)
site['to_space'] = date_to(2020,12,11)
site['app_name'] = '记录思考'
site['app_link'] = 'https://spacepage.top'

dispatch_path('../content/')
