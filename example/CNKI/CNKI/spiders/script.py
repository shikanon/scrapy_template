#coding:utf8
import random

nextpage_script = '''function main(splash)
    splash:go("http://epub.cnki.net/kns/oldnavi/n_list.aspx?NaviID=1&Field=168%u4e13%u9898%u4ee3%u7801&Value=I136%3f&OrderBy=idno&NaviLink=%u7535%u4fe1%u6280%u672f")
    splash:wait(1)
    splash:evaljs("__doPostBack('lbNextPage','')")
    splash:wait(1)
    return splash:html()
end'''


def to_page(num):
    if isinstance(num,int):
        script = '''function main(splash)
        splash:wait({random_number})
        splash:go("http://epub.cnki.net/kns/oldnavi/n_list.aspx?NaviID=1&Field=168%u4e13%u9898%u4ee3%u7801&Value=I136%3f&OrderBy=idno&NaviLink=%u7535%u4fe1%u6280%u672f")
        splash:wait(1)
        splash:evaljs("txtPageGoTo.value = {number};imgbtnGo[0].click()")
        splash:wait(1)
        return splash:html()
    end'''
        return script.format(random_number=random.random()*2, number=num)
