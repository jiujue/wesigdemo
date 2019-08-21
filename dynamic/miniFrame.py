import pymysql
import re
from urllib.request import quote,unquote
import setting

# remember change database password
def get_info(h=setting.DATABASE_IP, user=setting.DATABASE_USER, passwd=setting.DATABASE_PASSWD,
             db=setting.DATABASE_DB,sqlsentens="",sqlargs=None):
    try:

        conn=pymysql.Connect(host=h, user=user, password=passwd,
                         database=db)
        cursor=conn.cursor()
        if not sqlargs:
            cursor.execute(sqlsentens)
        else:
            cursor.execute(sqlsentens,sqlargs)
        res=cursor.fetchall()
        conn.commit()

        conn.close()
        cursor.close()
        return res
    except Exception as e:
        print("sql exception>>>",e)



funcMapping=dict()

def addFuncIntoDict(name):
    def replace(func):
        funcMapping[name] = func
        def add(*arg,**kwargs):
            pass
        return func
    return replace

@addFuncIntoDict("(/center.html)")
def center(env,set_hander_callback):
    info=get_info(sqlsentens="""select code,short,chg,turnover,price,
                    highs,note_info from info as i
                    inner join focus as f on i.id=f.info_id;""")
    tr_template = """
            <tr>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>
                    <a type="button" class="btn btn-default btn-xs" href="/update/%s.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
                </td>
                <td>
                    <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="%s">
                </td>
            </tr>
        """
    content = ""
    for it in info:
        content+=tr_template%(it[0],it[1],it[2],it[3],it[4],it[5],it[6],it[0],it[0])
    set_hander_callback(200, "OK", "text/html")
    print(env)

    with open(env["abspath"], "rb") as f:
        body=re.sub("{%content%}", content, f.read().decode("utf-8"))
    return body

@addFuncIntoDict("(/index.html)")
def index(env,set_hander_callback):
    info = get_info(sqlsentens="select * from info")
    tr_template = """<tr>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>
                <input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="%s">
            </td>
            </tr>
        """
    set_hander_callback(200, "OK", "text/html")
    print(env)
    content = ""
    for it in info:
        content += tr_template % (it[0], it[1], it[2], it[3], it[4], it[5], it[6], it[7],it[0])
    set_hander_callback(200, "OK", "text/html")
    print(env)

    with open(env["abspath"], "rb") as f:
        body = re.sub("{%content%}", content, f.read().decode("utf-8"))
    return body

@addFuncIntoDict("/add/(\d+?).html")
def addFocus(env,set_hander_callback):
    info_id=env["info_id"]
    res=get_info(sqlsentens="select * from focus where info_id like '%s'"%info_id)
    if not res:
        #can add
        res=get_info(sqlsentens="insert into focus (info_id)values(%s)"%info_id)
        print("----------SQL INsert %s res>>>>"%info_id,res)
        pass
    else:
        #can't add,focused
        return "以添加关注,请勿重复添加\nit have focused , not again"

    return env["info_id"]+" add ok"

@addFuncIntoDict("/del/(\d+?).html")
def delFocus(env,set_hander_callback):
    info_id=env["info_id"]
    res=get_info(sqlsentens=" select * from focus where info_id like (select id from info where code like '%s');"%info_id)
    if not res:
        #cna't delete focus

        return "从未拥有,何来忘记呢？\nNever owned, forget what?"
    else:
        #can delete focus
        res = get_info(sqlsentens=" delete from focus where info_id like (select id from info where code like '%s')" %info_id)
        print("----------SQL INsert %s res>>>>" % info_id, res)

    return env["info_id"]+" del ok"


# GET /update/600295.html HTTP/1.1
@addFuncIntoDict("/update/(\d+?).html")
def putUpdatePage(env,set_hander_callback):
    info_id=env["info_id"]
    res=get_info(sqlsentens="""select code,note_info
                            from focus as f
                            inner join info as i
                            on i.id=f.info_id
                            where i.code = '%s'"""%info_id)[0]
    try:
        with open(env["srcdir"]+"/update.html","rb") as f:
            content=f.read().decode("utf-8")

    except Exception as e:
        print("open file %s error -->"%env["srcdir"]+"update.html",e)
        return 404
    content=re.sub("{%code%}",res[0],content)
    content=re.sub("{%note_info%}",res[1],content)
    set_hander_callback(200, "OK", "text/html")
    return content

# GET /update/600295/hello%20update.html HTTP/1.1
@addFuncIntoDict("/update/(\d+?)/(.+).html")
def updateFocusNote(env,set_hander_callback):
    #update focus note
    res = get_info(sqlsentens="""update focus set note_info = '%s'
                                    where info_id = (select id from info
                                    where code like '%s')"""
                                    %(unquote(env["all_info"][1]),env["all_info"][0]))
    print("----------SQL Update  %s note_info res>>>>" % env['all_info'][0])

    return env["info_id"]+" change info  ok"


def matchp(path,env):
    for k, v in funcMapping.items():
        info=re.match(k, path)
        if info:
            env["info_id"]=info.group(1)
            env["all_info"]=info.groups()
            print( "-"*100,env["all_info"])
            return v


def application(env,set_hander_callback):

    func=matchp(env["path"],env)
    if not  func:
        set_hander_callback(404, "not found", "text/html")
        return 404
    else:
        return func(env,set_hander_callback)
