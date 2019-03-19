#!/usr/bin/env python3
# -*- coding: utf-8 -*-

html = '''
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
          hm.src = "https://hm.baidu.com/hm.js?{site[baidu_id]}";
          var s = document.getElementsByTagName("script")[0]; 
          s.parentNode.insertBefore(hm, s);
        }})();
    </script>
</head>
<body>
<header><p><a href="{site[app_link]}/">{site[app_name]}</a></p>
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
     <p>CopyRight &copy; <a href="{site[app_link]}/">{site[app_name]}</a></p>
</footer>
</body>
</html>
'''
