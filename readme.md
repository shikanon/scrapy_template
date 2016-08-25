# Genspider
#一个scrapy项目模板生成工具

--------------------
author: shikanon <shikanon@foxmail.com>
----------------------
一个scrapy项目生成工具，适合新手使用，可以生成一个scrapy基本模板，减少配置烦恼。
搭载了随机User-Agent，代理ip，redis等，
写入文件采用jsonline格式。

使用方法:
`python genspider.py`
`the new projects path:`在此输入生成的项目目录路径
`the projects name:`在此输入项目名称
转到项目目录下，执行
`scrapy list`
可以看到已生成的项目
运行`scrapy crawl 项目名称` 开始抓取任务。