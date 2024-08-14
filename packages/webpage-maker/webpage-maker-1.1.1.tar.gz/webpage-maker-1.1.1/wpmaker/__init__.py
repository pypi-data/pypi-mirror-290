#!/usr/bin/python
# -*- coding: utf-8 -*-

# Webpage Maker

# @Author:          WCF
# @LastEditTime:    2024-08-14 15:42:30
# @LastEditors:     WCF
# @Version:         1.1.1

__author__ = "WCF"
__version__ = "1.1.1"

print("\n----------------------------------")
print("|   WebpageMaker v1.1.1 by WCF   |")
print("| Modern, Simple and Easy to use |")
print("----------------------------------\n")
print("V1.1.1 logs:")
print("1. Rewrite the underlying escape logic;")
print("2. Add some explanations, and improve the code structure.")
print("3. Fixed some bugs.")
print("\n--------------------------------\n")


class newHtmlObj(object):
    def __init__(self,head="<title>Hello world!</title>\n", body="<h1>It's a HTML webpage!<body>\n", lang=None, v="5", dtd=""):
        self.code = ("<!DOCTYPE html>" if v=="5" else ("<!DOCTYPE HTML PUBLIC \""+dtd+"\">" if v=="4.01" else ("<!DOCTYPE html PUBLIC \""+dtd+"\">" if v=="xhtml 1.1" else "<!DOCTYPE HTML>")))+"\n<html"+(" lang=\""+lang+"\"" if lang else "")+">\n<head>\n"+head+"</head>\n<body>\n"+body+"</body>\n</html>"
        if v!="5" and v!="4.01" and v!="xhtml 1.1":
            print("Warning: The version of HTML is not supported, the default version (HTML5) will be used.")
        elif v=="4.01":
            print("Warning: The version of HTML being used is outdated and may not be supported by all browsers. It also cannot guarantee full support for all features of this module. It is not recommended to use it.")

def title(c):
    return("<title>%s</title>\n"%c)

def charset(t="utf-8"):
    return("<meta charset=\"%s\" />\n"%t)

def h(c="", l=1, **attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<h%s%s>%s</h%s>\n"%(l, attrs_str, c, l))

def comment(c):
    return("<!-- %s -->\n"%c)

def a(c="", **attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<a%s>%s</a>\n"%(attrs_str, c))

def abbr(c="", **attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<abbr%s>%s</abbr>\n"%(attrs_str, c))

def acronym(c="", **attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<acronym%s>%s</acronym>\n"%(attrs_str, c))

def address(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<address%s>%s</address>\n"%(attrs_str,c))

def applet(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<applet%s>%s</applet>\n"%(attrs_str,c))

def area(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<area%s>%s</area>\n"%(attrs_str,c))

def article(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<article%s>%s</article>\n"%(attrs_str,c))

def aside(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<aside%s>%s</aside>\n"%(attrs_str,c))

def audio(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<audio%s>%s</audio>\n"%(attrs_str,c))

def b(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<b%s>%s</b>\n"%(attrs_str,c))

def base(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<base%s>%s</base>\n"%(attrs_str,c))

def bdi(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<bdi%s>%s</bdi>\n"%(attrs_str,c))

def bdo(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<bdo%s>%s</bdo>\n"%(attrs_str,c))

def big(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<big%s>%s</big>\n"%(attrs_str,c))

def blockquote(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<blockquote%s>%s</blockquote>\n"%(attrs_str,c))

def body(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<body%s>%s</body>\n"%(attrs_str,c))

def br():
    return("<br \\>\n")

def button(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<button%s>%s</button>\n"%(attrs_str,c))

def canvas(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<canvas%s>%s</canvas>\n"%(attrs_str,c))

def caption(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<caption%s>%s</caption>\n"%(attrs_str,c))

def center(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<center%s>%s</center>\n"%(attrs_str,c))

def cite(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<cite%s>%s</cite>\n"%(attrs_str,c))

def code(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<code%s>%s</code>\n"%(attrs_str,c))

def col(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<col%s>%s</col>\n"%(attrs_str,c))

def colgroup(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<colgroup%s>%s</colgroup>\n"%(attrs_str,c))

def data(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<data%s>%s</data>\n"%(attrs_str,c))

def datalist(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<datalist%s>%s</datalist>\n"%(attrs_str,c)) 

def dd(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<dd%s>%s</dd>\n"%(attrs_str,c))

def del_(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<del%s>%s</del>\n"%(attrs_str,c))

def details(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<details%s>%s</details>\n"%(attrs_str,c))

def dfn(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<dfn%s>%s</dfn>\n"%(attrs_str,c))

def dialog(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<dialog%s>%s</dialog>\n"%(attrs_str,c))

def div(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<div%s>%s</div>\n"%(attrs_str,c))

def dir(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<dir%s>%s</dir>\n"%(attrs_str,c))

def dl(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<dl%s>%s</dl>\n"%(attrs_str,c))

def dt(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<dt%s>%s</dt>\n"%(attrs_str,c))

def em(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<em%s>%s</em>\n"%(attrs_str,c))

def embed(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<embed%s>%s</embed>\n"%(attrs_str,c))

def fencedframe(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<fencedframe%s>%s</fencedframe>\n"%(attrs_str,c))

def fieldset(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<fieldset%s>%s</fieldset>\n"%(attrs_str,c))

def figcaption(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<figcaption%s>%s</figcaption>\n"%(attrs_str,c))

def figure(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<figure%s>%s</figure>\n"%(attrs_str,c))

def font(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<font%s>%s</font>\n"%(attrs_str,c))

def footer(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<footer%s>%s</footer>\n"%(attrs_str,c))

def form(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<form%s>%s</form>\n"%(attrs_str,c))

def frame(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<frame%s>%s</frame>\n"%(attrs_str,c))

def frameset(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<frameset%s>%s</frameset>\n"%(attrs_str,c))

def h1(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<h1%s>%s</h1>\n"%(attrs_str,c))

def h2(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<h2%s>%s</h2>\n"%(attrs_str,c))

def h3(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<h3%s>%s</h3>\n"%(attrs_str,c))

def h4(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<h4%s>%s</h4>\n"%(attrs_str,c))

def h5(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<h5%s>%s</h5>\n"%(attrs_str,c))

def h6(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<h6%s>%s</h6>\n"%(attrs_str,c))

def head(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<head%s>%s</head>\n"%(attrs_str,c))

def header(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<header%s>%s</header>\n"%(attrs_str,c))

def hr():
    return("<hr \>\n")

def html(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<html%s>%s</html>\n"%(attrs_str,c))

def i(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<i%s>%s</i>\n"%(attrs_str,c))

def iframe(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<iframe%s>%s</iframe>\n"%(attrs_str,c))

def img(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<img%s>%s</img>\n"%(attrs_str,c))

def input_(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<input%s>%s</input>\n"%(attrs_str,c))

def ins(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<ins%s>%s</ins>\n"%(attrs_str,c))

def kbd(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<kbd%s>%s</kbd>\n"%(attrs_str,c))

def label(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<label%s>%s</label>\n"%(attrs_str,c))

def legend(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<legend%s>%s</legend>\n"%(attrs_str,c))

def li(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<li%s>%s</li>\n"%(attrs_str,c))

def link(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<link%s>%s</link>\n"%(attrs_str,c))

def main(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<main%s>%s</main>\n"%(attrs_str,c))

def map_(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<map%s>%s</map>\n"%(attrs_str,c))

def mark(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<mark%s>%s</mark>\n"%(attrs_str,c))

def marquee(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<marquee%s>%s</marquee>\n"%(attrs_str,c))

def menu(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<menu%s>%s</menu>\n"%(attrs_str,c))

def meta(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<meta%s>%s</meta>\n"%(attrs_str,c))

def meter(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<meter%s>%s</meter>\n"%(attrs_str,c))

def nav(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<nav%s>%s</nav>\n"%(attrs_str,c))

def nobr(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<nobr%s>%s</nobr>\n"%(attrs_str,c))

def noembed(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<noembed%s>%s</noembed>\n"%(attrs_str,c))

def noframes(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<noframes%s>%s</noframes>\n"%(attrs_str,c))

def noscript(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<noscript%s>%s</noscript>\n"%(attrs_str,c))

def object_(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<object%s>%s</object>\n"%(attrs_str,c))

def ol(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<ol%s>%s</ol>\n"%(attrs_str,c))

def optgroup(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<optgroup%s>%s</optgroup>\n"%(attrs_str,c))

def option(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<option%s>%s</option>\n"%(attrs_str,c))

def output(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<output%s>%s</output>\n"%(attrs_str,c))

def p(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<p%s>%s</p>\n"%(attrs_str,c))

def param(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<param%s>%s</param>\n"%(attrs_str,c))

def picture(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<picture%s>%s</picture>\n"%(attrs_str,c))

def plaintext(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<plaintext%s>%s</plaintext>\n"%(attrs_str,c))

def portal(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<portal%s>%s</portal>\n"%(attrs_str,c))

def pre(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<pre%s>%s</pre>\n"%(attrs_str,c))

def progress(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<progress%s>%s</progress>\n"%(attrs_str,c))

def q(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<q%s>%s</q>\n"%(attrs_str,c))

def rb(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<rb%s>%s</rb>\n"%(attrs_str,c))

def rp(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<rp%s>%s</rp>\n"%(attrs_str,c))

def rt(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<rt%s>%s</rt>\n"%(attrs_str,c))

def rtc(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<rtc%s>%s</rtc>\n"%(attrs_str,c))

def ruby(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<ruby%s>%s</ruby>\n"%(attrs_str,c))

def s(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<s%s>%s</s>\n"%(attrs_str,c))

def samp(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<samp%s>%s</samp>\n"%(attrs_str,c))

def script(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<script%s>%s</script>\n"%(attrs_str,c))

def section(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<section%s>%s</section>\n"%(attrs_str,c))

def select(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<select%s>%s</select>\n"%(attrs_str,c))

def small(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<small%s>%s</small>\n"%(attrs_str,c))

def source(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<source%s>%s</source>\n"%(attrs_str,c))

def span(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<span%s>%s</span>\n"%(attrs_str,c))

def strike(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<strike%s>%s</strike>\n"%(attrs_str,c))

def strong(c="",**attrs):                                                                                                                                                                                                                               
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<strong%s>%s</strong>\n"%(attrs_str,c))

def style(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<style%s>%s</style>\n"%(attrs_str,c))

def sub(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<sub%s>%s</sub>\n"%(attrs_str,c))

def summary(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<summary%s>%s</summary>\n"%(attrs_str,c))

def sup(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<sup%s>%s</sup>\n"%(attrs_str,c))

def table(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<table%s>%s</table>\n"%(attrs_str,c))

def tbody(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<tbody%s>%s</tbody>\n"%(attrs_str,c))

def td(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<td%s>%s</td>\n"%(attrs_str,c))

def template(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<template%s>%s</template>\n"%(attrs_str,c))

def textarea(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<textarea%s>%s</textarea>\n"%(attrs_str,c))

def tfoot(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<tfoot%s>%s</tfoot>\n"%(attrs_str,c))

def th(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<th%s>%s</th>\n"%(attrs_str,c))

def thead(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<thead%s>%s</thead>\n"%(attrs_str,c))

def time(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<time%s>%s</time>\n"%(attrs_str,c))

def title(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<title%s>%s</title>\n"%(attrs_str,c))

def tr(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<tr%s>%s</tr>\n"%(attrs_str,c))

def track(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<track%s>%s</track>\n"%(attrs_str,c))

def tt(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<tt%s>%s</tt>\n"%(attrs_str,c))

def u(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<u%s>%s</u>\n"%(attrs_str,c))

def ul(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<ul%s>%s</ul>\n"%(attrs_str,c))

def var(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<var%s>%s</var>\n"%(attrs_str,c))

def video(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<video%s>%s</video>\n"%(attrs_str,c))

def wbr(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<wbr%s>%s</wbr>\n"%(attrs_str,c))

def xmp(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<xmp%s>%s</xmp>\n"%(attrs_str,c))


def javascript(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<script%s type=\"text/javascript\">%s</script>\n"%(attrs_str,c))

def babel(c="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<script%s type=\"text/babel\">%s</script>\n"%(attrs_str,c))

def referenceJS(src="",**attrs):
    attrs_str = ""
    for attr in attrs.items():
        attrs_str += " %s=\"%s\""%(attr[0][:-1] if attr[0].endswith("_") else attr[0],attr[1])
    return("<script%s type=\"text/javascript\" src=\"%s\"></script>\n"%(attrs_str,src))


js = javascript
babeljs = babel
refjs = referenceJS
refJs = referenceJS
rjs = referenceJS
rJs = referenceJS
nextLine = br()
nextLine_ = br

