#
# funcDict=dict()
# def addFuncIntoDict(name):
#     def replace(func):
#         funcDict[name] = func
#         def add(*arg,**kwargs):
#             pass
#         return func
#     return replace
#
# @addFuncIntoDict("dir")
# def go(*arg,**kwargs):
#         print("outer",*arg,**kwargs)
#
# print("call befor",funcDict)
# go("hwllo python")
# print("call after",funcDict)
# funcDict["dir"]()


#





# import re
#
# funcdict={'(/center.html)': "<function center at 0x00000229AF2C8730>",
#           '(/index.html)': "<function index at 0x00000229AF2C87B8>",
#           '/add/(\\d+).html': "<function addFocus at 0x00000229AF2C8840>"}
#
# def matchp(path):
#     for k,v in funcdict.items():
#         mp=re.match(k, path)
#         if mp:
#             print(mp.group(1))
#             print()
#
# matchp("/center.html")

# import pymysql
# def get_info(h="127.0.0.1", user="root", passwd="111111",
#              db="stock_db",sql="select id ,code from info where code like '000007'"):
#     conn=pymysql.Connect(host=h, user=user, password=passwd,
#                      database=db)
#     cursor=conn.cursor()
#     cursor.execute(sql)
#     return cursor.fetchall()
#
# print(get_info()[0][0])

# import urllib.parse as parse
#
# parse.quote()
# parse.unquote()
# import pymysql
# def get_info(h="127.0.0.1", user="root", passwd="111111",
#              db="stock_db",sqlsentens=None):
#     conn=pymysql.Connect(host=h, user=user, password=passwd,
#                      database=db)
#     cursor=conn.cursor()
#     cursor.execute(sqlsentens)
#     return cursor.fetchall()
#
# res=get_info(sqlsentens="""select code,note_info
#                             from focus as f
#                             inner join info as i
#                             on i.id=f.info_id
#                             where i.code = 600295""")
# print(res[0][0],res[0][1])
# import re
# from urllib.request import quote,unquote
# str="""            </tr>
#             {%content%}
#         </table>
#     </div>"""
# mp=re.sub("{%content%}","nihao",str)
# srcq='/update/(\d+?)/(.+).html'
# mp=re.match(srcq,"/update/600295/mpmp%20%20%20mmp.html")
# print(mp.groups()[0],unquote(mp.groups()[1]))
import time
log=open("./log.log","ba")
def set(func,level="d"):
    """
    :param func:
    :param level: e->error ,d->debug, n->normal
    :return:
    """
    def mp(*args):
        func(("["+time.ctime()+"] "+" [>Normal<] "+"[: ").encode("utf-8"))
        func(str(*args).encode("utf-8"))
        func(("]\n").encode("utf-8"))
    return mp
print=set(log.write,)



