'''
预提供的
youdao-appid: 15f45a64cbf74042
appsecret: iS0Mz8CxDJcgIKkxNdCfMDxITvliKO5e
文件夹根目录下有已做好的相关db，修改文件名或复制副本即可使用

Author>>中英单词翻译，存储与测试系统
Author>>Kid_Ocelot Kid豹猫 制作
Author>>需求可用的有道翻译api来使用全部功能
'''

import sqlite3
import sys
import uuid
import requests
import hashlib
import time
from importlib import reload
import json
import time
import random

def connect_db(db_input):
    if db_input == "empty":
        db=sqlite3.connect("Words.db")
        db.execute("CREATE TABLE youdao (appID TEXT,appSECRET TEXT,access INTEGER)")
        db.execute("CREATE TABLE new (CN TEXT,EN TEXT,value INTEGER DEFAULT(0))")
        db.execute("CREATE TABLE prob (CN TEXT,EN TEXT,value INTEGER DEFAULT(0))")
        db.execute("CREATE TABLE fin (CN TEXT,EN TEXT)")
        #db.execute("INSERT INTO youdao (id,appID,appSECRET) values (1,'" + appID + "','" + appSECRET + "')")
        #db.execute("INSERT INTO youdao (id,appID,appSECRET) values (1,'text','text2')")
        db.execute("INSERT into youdao(access) values(0)")
    else:
        db=sqlite3.connect(db_input)
    return db

def db_verification(db):
    #Only Verify Colomns
    errors=0
    try:
        db.execute("SELECT appID,appSECRET,access from youdao")
    except sqlite3.OperationalError:
        print("Veri>>表Youdao出错")
        errors=errors+1
    try:
        db.execute("SELECT CN,EN,value from new")
    except sqlite3.OperationalError:
        print("Veri>>表new出错")
        errors=errors+1
    try:
        db.execute("SELECT CN,EN,value from prob")
    except sqlite3.OperationalError:
        print("Veri>>表prob出错")
        errors=errors+1
    try:
        db.execute("SELECT CN,EN from fin")
    except sqlite3.OperationalError:
        print("Veri>>表fin出错")
        errors=errors+1
    print("Veri>>找到",errors,"个错误.")
    if errors>0:
        print("Veri>>",errors,"个错误被发现，试着创建一个新的数据库？",end="\n\n")
    else:
        print("Veri>>验证通过.",end="\n\n")

def mainChoice():
    print("Main>>选择操作.")
    print("Main>>1:配置有道api相关")
    print("Main>>2:翻译自选词语")
    print("Main>>3:单词管理")
    print("Main>>4:单词测试")
    print("Main>>5:单词表间迁移")
    print("Main>>6")
    print("Main>>7")
    print("Main>>8")
    print("Main>>9:帮助")
    print("Main>>10:关闭数据库")
    sel=str(input("Main>>操作序号:"))
    return sel

def youdaoGlobalinfoRefresh():
    youdao_appID=db.execute("Select appID from youdao").fetchone()[0]
    youdao_appSECRET=db.execute("Select appSECRET from youdao").fetchone()[0]
    return youdao_appID,youdao_appSECRET

def fetchlist(database,table):#Usage(db,new) Return(Indexs count,Selection)
    list_=database.execute("SELECT * from "+str(table)).fetchall()
    recur=0
    while True:
            try:
                list_[recur]
                recur=recur+1
            except:
                break
    return recur,list_

###################################youdao-request copied from ai.youdao.com (modified)
def youdaoRequest(q,APP_KEY,APP_SECRET,destni_lang="en"):
    import sys
    import uuid
    import requests
    import hashlib
    import time
    from importlib import reload
    import json
    import time

    reload(sys)

    YOUDAO_URL = 'https://openapi.youdao.com/api'
    
    def encrypt(signStr):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(signStr.encode('utf-8'))
        return hash_algorithm.hexdigest()


    def truncate(q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


    def do_request(data):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(YOUDAO_URL, data=data, headers=headers)


    def connect(q):
    #    q = "有道智云控制台"

        data = {}
        data['from'] = 'auto'
        data['to'] = destni_lang
        data['signType'] = 'v3'
        curtime = str(int(time.time()))
        data['curtime'] = curtime
        salt = str(uuid.uuid1())
        signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
        sign = encrypt(signStr)
        data['appKey'] = APP_KEY
        data['q'] = q
        data['salt'] = salt
        data['sign'] = sign
        data['vocabId'] = "9E47A57AA8B348B789AD6C59B94AFA79"

        response = do_request(data)
        return response.content

    youdao_return=connect(q)
    youdao_return=youdao_return.decode()
    youdao_return=json.loads(youdao_return)
    return youdao_return["translation"][0],youdao_return["errorCode"],youdao_return
#################################################youdao-request########Define part ends
print("""
Author>>中英单词翻译，存储与测试系统
Author>>Kid_Ocelot Kid豹猫 制作
Author>>需求可用的有道翻译api来使用全部功能
""")

db_int_sel=str(input("Conn>>1:连接数据库 2（默认）：创建数据库 输入："))
if db_int_sel=="1":
    db=connect_db(str(input("Conn>>数据库名称（xxxx.db）：")))
    #db=connect_db("Words.db")#Fast testment,Changing later
else:
    db=connect_db("empty")
    print("Conn>>已创建新数据库.",end="\n\n")
print("Veri>>数据库已链接，正在验证.")
db_verification(db)

#During the main Program, Don't forget to db.commit()!

while True:
    youdao_veri=0
    youdao_res_veri1=db.execute("Select appID from youdao").fetchone()[0]
    youdao_res_veri2=db.execute("Select appSECRET from youdao").fetchone()[0]
    if youdao_res_veri1 == None or youdao_res_veri2 == None:
        print("Main>>有道api信息未找到.",end="\n\n")
        youdao_veri=1
    else:
        #Refresh app algorithm
        youdao_appID=youdaoGlobalinfoRefresh()[0]
        youdao_appSECRET=youdaoGlobalinfoRefresh()[1]
        if db.execute("SELECT access from youdao").fetchone()[0]!=1:
            print("Main>>有道api信息找到但未验证.",end="\n\n")
    sel=mainChoice()
    print()#\n
    if sel=="1":#Youdao id Config
        youdao_sel_main=str(input("Youdao>>1:输入新的信息 2:查看当前信息与状态 3:验证当前信息 选择："))
        if youdao_sel_main=="1":
            print("Youdao>>现在输入新的信息.")
            youdao_res_appID=str(input("Youdao>>appID:"))
            youdao_res_appSECRET=str(input("Youdao>>appSECRET:"))
            if youdao_veri!=1:
                print("Youdao>>清除了旧的信息.")
                db.execute("Delete from youdao")
                db.execute("Insert into youdao(access) values(0)")

            db.execute("Update youdao Set appID='"+youdao_res_appID+"',appSECRET='"+youdao_res_appSECRET+"',access=0")
            #db.execute("Insert into youdao (appID,appSECRET) values ('"+youdao_res_appID+"','"+youdao_res_appSECRET+"')")
            #db.execute("UPDATE youdao SET access=0")
            print("Youdao>>成功输入了新信息.",end="\n\n")
            db.commit()
        if youdao_sel_main=="2":
            print("Youdao>>现在查看当前信息")
            if youdao_veri==1:
                print("Youdao>>未找到已输入的信息.")
            youdao_check_appid=db.execute("Select appID from youdao").fetchone()
            youdao_check_appsec=db.execute("Select appSECRET from youdao").fetchone()
            youdao_check_appaccess=db.execute("SELECT access from youdao").fetchone()
            if youdao_check_appaccess[0]==1:
                youdao_check_appaccess="可用"
            else:
                youdao_check_appaccess="不可用"
            print("Youdao>>appID:",youdao_check_appid[0])
            print("Youdao>>appSECRET:",youdao_check_appsec[0])
            print("Youdao>>可用性:",youdao_check_appaccess)
            print("Youdao>>成功查看了当前的信息.",end="\n\n")
        if youdao_sel_main=="3":
            print("Youdao>>现在验证当前信息的可用性.")
            if youdao_veri==1:
                print("Youdao>>未找到已输入的信息.")
            if youdao_veri==0:
                try:
                    youdao_accessbility=youdaoRequest("apple",youdao_appID,youdao_appSECRET,"zh-CHS")#zh-CHS/en
                except:
                    print("Youdao>>可用性测试未通过.",end="\n\n")
                    youdao_accessbility=("error")
                if youdao_accessbility[1]=="0":
                    print("Youdao>>可用性测试通过.",end="\n\n")
                    db.execute("UPDATE youdao SET access=1")
                    db.commit()
    if sel=="2":#Translation
        trans_veri_access=db.execute("Select access from youdao").fetchone()[0]
        if trans_veri_access!=1:
            print("Trans>>请先通过Main>>有道>>可用性 中的可用性测试.")
        else:
            trans_type_sel=str(input("Trans>>选择目标语言 1:英语 2:中文 选择："))
            trans_query=str(input("Trans>>输入内容："))
            if trans_type_sel != "2":
                trans_type_sel="en"
            else:
                trans_type_sel="zh-CHS"
            print("Trans>>翻译为：",str(youdaoRequest(trans_query,youdao_appID,youdao_appSECRET,trans_type_sel)[0]),end="\n\n")
    if sel=="3":#Manage Words
        mana_sel_main=str(input("Manage>>1:输入新的词语 2:查看当前词库 选择："))
        if mana_sel_main=="1":
            print("Manage>>输入方法仅适用于表new，执行更多操作请使用SQlite Studio.")
            #mana>>inp>>Selecion matrix

            #Check accessbility
            if db.execute("SELECT access from youdao").fetchone()[0]==1:
                mana_sel_Input_youdao=str(input("Manage>>Input>>选择输入值是否自动翻译 1:自动翻译 2:手动输入 选择："))
            else:
                mana_sel_Input_youdao="2"
            mana_sel_Input_method=str(input("Manage>>Input>>选择输入方法 1:单个 2:多个（输入空值/回车 来取消该模式） 选择："))
            #Once AutoYoudao isn't chosen,Input Preference==CN
            #a.k.a "212" & "222" choices can't be chosen
            #Down there "122" "222" can't be chosen
            #Down there "212"&"222" are the same

            if mana_sel_Input_youdao=="1":
                mana_sel_Input_preference=str(input("Manage>>Input>>选择输入的语言 1:中文 2:英语"))
            else:
                mana_sel_Input_preference="1"

            mana_char_en=""
            mana_char_cn=""
            mana_count=0
            if mana_sel_Input_method=="1" and mana_sel_Input_preference=="1" and mana_sel_Input_youdao=="1":
                mana_char_cn=str(input("Manage>>Input>>输入中文："))
                mana_char_en=str(youdaoRequest(mana_char_cn,youdao_appID,youdao_appSECRET,"en")[0])
                db.execute("Insert into new(CN,EN) values('"+mana_char_cn+"','"+mana_char_en+"')")
                print("Manage>>Input>>成功输入了  "+mana_char_cn+" , "+mana_char_en)
            if mana_sel_Input_method=="1" and mana_sel_Input_preference=="1" and mana_sel_Input_youdao=="2": #same as 222
                mana_char_cn=str(input("Manage>>Input>>输入中文："))
                mana_char_en=str(input("Manage>>Input>>输入英文："))
                db.execute("Insert into new(CN,EN) values('"+mana_char_cn+"','"+mana_char_en+"')")
                print("Manage>>Input>>成功输入了  "+mana_char_cn+" , "+mana_char_en,end="\n\n")
            if mana_sel_Input_method=="1" and mana_sel_Input_preference=="2" and mana_sel_Input_youdao=="1":
                mana_char_en=str(input("Manage>>Input>>输入英文："))
                mana_char_cn=str(youdaoRequest(mana_char_en,youdao_appID,youdao_appSECRET,"zh-CHS")[0])
                db.execute("Insert into new(CN,EN) values('"+mana_char_cn+"','"+mana_char_en+"')")
                print("Manage>>Input>>成功输入了  "+mana_char_cn+" , "+mana_char_en,end="\n\n")
            if mana_sel_Input_method=="1" and mana_sel_Input_preference=="2" and mana_sel_Input_youdao=="2": #same as 212 #Can't be chosen
                mana_char_cn=str(input("Manage>>Input>>输入中文："))
                mana_char_en=str(input("Manage>>Input>>输入英文："))
                db.execute("Insert into new(CN,EN) values('"+mana_char_cn+"','"+mana_char_en+"')")
                print("Manage>>Input>>成功输入了  "+mana_char_cn+" , "+mana_char_en,end="\n\n")
            if mana_sel_Input_method=="2" and mana_sel_Input_preference=="1" and mana_sel_Input_youdao=="1":#cn2en
                mana_count=0
                while True:
                    mana_char_cn=str(input("Manage>>Input>>输入中文："))
                    if mana_char_cn=="":
                        print("Manage>>Input>>退出输入模式， "+str(mana_count)+"  个词被输入.",end="\n\n")
                        break
                    else:
                        mana_char_en=str(youdaoRequest(mana_char_cn,youdao_appID,youdao_appSECRET,"en")[0])
                        db.execute("Insert into new(CN,EN) values('"+mana_char_cn+"','"+mana_char_en+"')")
                        print("Manage>>Input>>成功输入了  "+mana_char_cn+" , "+mana_char_en,end="\n\n")
                        mana_count=mana_count+1
            if mana_sel_Input_method=="2" and mana_sel_Input_preference=="1" and mana_sel_Input_youdao=="2":#Same as 122
                mana_count=0
                while True:
                    mana_char_cn=str(input("Manage>>Input>>输入中文："))
                    mana_char_en=str(input("Manage>>Input>>输入英文："))
                    if mana_char_cn=="" or mana_char_en=="":
                        print("Manage>>Input>>退出输入模式， "+str(mana_count)+"  个词被输入.",end="\n\n")
                        break
                    else:
                        db.execute("Insert into new(CN,EN) values('"+mana_char_cn+"','"+mana_char_en+"')")
                        print("Manage>>Input>>成功输入了  "+mana_char_cn+" , "+mana_char_en,end="\n\n")
                        mana_count=mana_count+1
            if mana_sel_Input_method=="2" and mana_sel_Input_preference=="2" and mana_sel_Input_youdao=="1":#e
                mana_count=0
                while True:
                    mana_char_en=str(input("Manage>>Input>>输入英文："))
                    if mana_char_en=="":
                        print("Manage>>Input>>退出输入模式， "+str(mana_count)+"  个词被输入.",end="\n\n")
                        break
                    else:
                        mana_char_cn=str(youdaoRequest(mana_char_en,youdao_appID,youdao_appSECRET,"zh-CHS")[0])
                        db.execute("Insert into new(CN,EN) values('"+mana_char_cn+"','"+mana_char_en+"')")
                        print("Manage>>Input>>成功输入了  "+mana_char_cn+" , "+mana_char_en,end="\n\n")
                        mana_count=mana_count+1
                if mana_sel_Input_method=="2" and mana_sel_Input_preference=="2" and mana_sel_Input_youdao=="2":#Same as 112 Can't be chosen
                    mana_count=0
                    while True:
                        mana_char_cn=str(input("Manage>>Input>>输入中文："))
                        mana_char_en=str(input("Manage>>Input>>输入英文："))
                        if mana_char_cn=="" or mana_char_en=="":
                            print("Manage>>Input>>退出输入模式， "+str(mana_count)+"  个词被输入.",end="\n\n")
                            break
                        else:
                            db.execute("Insert into new(CN,EN) values('"+mana_char_cn+"','"+mana_char_en+"')")
                            print("Manage>>Input>>成功输入了  "+mana_char_cn+" , "+mana_char_en,end="\n\n")
                            mana_count=mana_count+1
            db.commit()
        if mana_sel_main=="2":#View tables
            mana_view_tuple=fetchlist(db,"new")[1]
            mana_recur_int=fetchlist(db,"new")[0]
            print("Manage>>View>>有",mana_recur_int,"个词在表new中.")
            for i in range(0,mana_recur_int,1):
                print("Manage>>View>>表 new: CN:",mana_view_tuple[i][0],", EN:",mana_view_tuple[i][1],", Rank:",mana_view_tuple[i][2])
            print()#\n
            
            mana_view_tuple=fetchlist(db,"prob")[1]
            mana_recur_int=fetchlist(db,"prob")[0]
            print("Manage>>View>>有",mana_recur_int,"个词在表prob中.")
            for i in range(0,mana_recur_int,1):
                print("Manage>>View>>表 prob: CN:",mana_view_tuple[i][0],", EN:",mana_view_tuple[i][1],", Rank:",mana_view_tuple[i][2])
            print()#\n
            
            mana_view_tuple=fetchlist(db,"fin")[1]
            mana_recur_int=fetchlist(db,"fin")[0]
            print("Manage>>View>>有",mana_recur_int,"个词在表fin中.")
            for i in range(0,mana_recur_int,1):
                print("Manage>>View>>表 new: CN:",mana_view_tuple[i][0],", EN:",mana_view_tuple[i][1])
            print()#\n
    if sel=="4":#Do tests
        print("Tests>>进入了测试模式，输入空值/回车来退出.")
        test_sel_main=str(input("Tests>>选择测试的表 1:new 2:prob 选择:"))
        test_success=0#Init
        test_failure=0#Init
        if test_sel_main!="2":#New
            test_count=fetchlist(db,"new")[0]
            if test_count>0:
                while True:
                    test_list=fetchlist(db,"new")[1]
                    test_random_1=int(random.randint(0,test_count-1))
                    test_req=""
                    try:
                        test_req=test_list[test_random_1]
                    except:
                        break
                    test_answer_EN=str(input("Tests>>把 "+str(test_req[0])+" 翻译成英语."))
                    if test_answer_EN=="":
                        print("Tests>>已退出测试模式. 这次测试有 "+str(test_success)+" 次成功与 "+str(test_failure)+" 次失败.")
                        break
                    if test_answer_EN==str(test_req[1]):
                        test_success=test_success+1
                        db.execute("UPDATE new SET value="+str(test_req[2]+1)+" WHERE CN='"+test_req[0]+"'")#Success=>+1
                        db.commit()
                        print("Test>>正确.",end="\n\n")
                    else:
                        test_failure=test_failure+1
                        db.execute("UPDATE new SET value="+str(test_req[2]-1)+" WHERE CN='"+test_req[0]+"'")#Fail=>-1
                        db.commit()
                        print("Test>>错误. 正确答案是 "+str(test_req[1])+" .",end="\n\n")
                    db.commit()
            else:
                print("Tests>>表new中没有词汇.",end="\n\n")

                
        if test_sel_main=="2":#Prob
            test_count=fetchlist(db,"prob")[0]
            if test_count>0:
                while True:
                    test_list=fetchlist(db,"prob")[1]
                    test_random_1=int(random.randint(0,test_count-1))
                    test_req=""
                    try:
                        test_req=test_list[test_random_1]
                    except:
                        break
                    test_answer_EN=str(input("Tests>>把 "+str(test_req[0])+" 翻译成英语."))
                    if test_answer_EN=="":
                        print("Tests>>已退出测试模式. 这次测试有 "+str(test_success)+" 次成功与 "+str(test_failure)+" 次失败.")
                        break
                    if test_answer_EN==str(test_req[1]):
                        test_success=test_success+1
                        db.execute("UPDATE prob SET value="+str(test_req[2]+1)+" WHERE CN='"+test_req[0]+"'")#Success=>+1
                        db.commit()
                        print("Test>>正确.",end="\n\n")
                    else:
                        test_failure=test_failure+1
                        db.execute("UPDATE prob SET value="+str(test_req[2]-1)+" WHERE CN='"+test_req[0]+"'")#Fail=>-1
                        db.commit()
                        print("Test>>错误.正确答案是 "+str(test_req[1])+" .",end="\n\n")
                    db.commit()
            else:
                print("Tests>>表prob中没有词汇.",end="\n\n")
    if sel=="5":#Migration
        mig_count=0
        mig_list_new=fetchlist(db,"new")
        mig_list_prob=fetchlist(db,"prob")
        mig_list_fin=fetchlist(db,"fin")
        mig_sel=str(input("Mig>>选择转表方向. 1:new>prob 2.new>fin 3:prob>new 选择："))##Guideline
        if mig_sel=="1":#new>>prob
            #Copied from View
            mig_mana_view_tuple=fetchlist(db,"new")[1]
            mig_mana_recur_int=fetchlist(db,"new")[0]
            print("Mig>>View>>",mig_mana_recur_int,"个词在表new中.")
            for i in range(0,mig_mana_recur_int,1):
                print("Mig>>View>>表 new: CN:",mig_mana_view_tuple[i][0],", EN:",mig_mana_view_tuple[i][1],"Count:",mig_mana_view_tuple[i][2])
            print()#\n
            
            mig_mana_view_tuple=fetchlist(db,"prob")[1]
            mig_mana_recur_int=fetchlist(db,"prob")[0]
            print("Mig>>View>>",mig_mana_recur_int,"个词在表prob中.")
            for i in range(0,mig_mana_recur_int,1):
                print("Mig>>View>>表 prob: CN:",mig_mana_view_tuple[i][0],", EN:",mig_mana_view_tuple[i][1],"Count:",mig_mana_view_tuple[i][2])
            print()#\n
            
            mig_1_sel=int(input("Mig>>输入 'Count' 的最大值. 如果输入3的话，所有'Count'<=3的值都会被迁移. 输入："))
            for i in range(0,mig_list_new[0],1):
                if mig_list_new[1][i][2]<=mig_1_sel:
                    db.execute("DELETE FROM new WHERE en = '"+mig_list_new[1][i][1]+"'")
                    db.execute("INSERT INTO prob (cn,en,value) values ('"+mig_list_new[1][i][0]+"','"+mig_list_new[1][i][1]+"',"+str(mig_list_new[1][i][2])+")")
                    print("Mig>>迁移了 ",mig_list_new[1][i])
                    mig_count=mig_count+1
            print("Mig>>迁移了 ",mig_count," 个词.",end="\n\n")

        
        if mig_sel=="2":#new>>fin
            mig_mana_view_tuple=fetchlist(db,"new")[1]
            mig_mana_recur_int=fetchlist(db,"new")[0]
            print("Mig>>View>>",mig_mana_recur_int,"个词在表new中.")
            for i in range(0,mig_mana_recur_int,1):
                print("Mig>>View>>表 new: CN:",mig_mana_view_tuple[i][0],", EN:",mig_mana_view_tuple[i][1],"Count:",mig_mana_view_tuple[i][2])
            print()#\n
            
            mig_mana_view_tuple=fetchlist(db,"fin")[1]
            mig_mana_recur_int=fetchlist(db,"fin")[0]
            print("Mig>>View>>",mig_mana_recur_int,"个词在表fin中.")
            for i in range(0,mig_mana_recur_int,1):
                print("Mig>>View>>表 fin: CN:",mig_mana_view_tuple[i][0],", EN:",mig_mana_view_tuple[i][1])
            print()#\n
            
            mig_2_sel=int(input("Mig>>输入 'Count' 的最小值. 如果输入3的话，所有'Count'>=3的值都会被迁移. 输入："))
            for i in range(0,mig_list_new[0],1):
                if mig_list_new[1][i][2]>=mig_2_sel:
                    db.execute("DELETE FROM new WHERE en = '"+mig_list_new[1][i][1]+"'")
                    db.execute("INSERT INTO fin (cn,en) values ('"+mig_list_new[1][i][0]+"','"+mig_list_new[1][i][1]+"')")
                    print("Mig>>迁移了 ",mig_list_new[1][i])
                    mig_count=mig_count+1
            print("Mig>>迁移了 ",mig_count," 个词.",end="\n\n")

        if mig_sel=="3":#prob>>new
            #Copied from View
            mig_mana_view_tuple=fetchlist(db,"prob")[1]
            mig_mana_recur_int=fetchlist(db,"prob")[0]
            print("Mig>>View>>",mig_mana_recur_int,"个词在表prob中")
            for i in range(0,mig_mana_recur_int,1):
                print("Mig>>View>>表 prob: CN:",mig_mana_view_tuple[i][0],", EN:",mig_mana_view_tuple[i][1],"Count:",mig_mana_view_tuple[i][2])
            print()#\n
            
            mig_mana_view_tuple=fetchlist(db,"new")[1]
            mig_mana_recur_int=fetchlist(db,"new")[0]
            print("Mig>>View>>",mig_mana_recur_int,"个词在表new中")
            for i in range(0,mig_mana_recur_int,1):
                print("Mig>>View>>表 new: CN:",mig_mana_view_tuple[i][0],", EN:",mig_mana_view_tuple[i][1],"Count:",mig_mana_view_tuple[i][2])
            print()#\n
            
            mig_3_sel=int(input("Mig>>输入 'Count' 的最小值. 如果输入3的话，所有'Count'>=3的值都会被迁移. 输入："))
            for i in range(0,mig_list_prob[0],1):
                if mig_list_prob[1][i][2]>=mig_3_sel:
                    db.execute("DELETE FROM prob WHERE en = '"+mig_list_prob[1][i][1]+"'")
                    db.execute("INSERT INTO new (cn,en,value) values ('"+mig_list_prob[1][i][0]+"','"+mig_list_prob[1][i][1]+"',"+str(mig_list_prob[1][i][2])+")")
                    print("Mig>>迁移了 ",mig_list_prob[1][i])
                    mig_count=mig_count+1
            print("Mig>>迁移了 ",mig_count," 个词.",end="\n\n")

    if sel=="9":#Help
        print("Help>>1:关于Youdao-id与翻译")
        print("Help>>2:关于数据库")
        help_sel_main=str(input("Help>>选择捏:"))
        if help_sel_main=="1":
            print("Help>>有道id是去ai.youdao.com进行一个带文本翻译api的app的申请")
            print("Help>>并且将其中的appid与appsecret进行一个Main>>Youdao>>New>>那边的输入")
            print("Help>>然后主界面的Appid/secMissing就会变成Not verified")
            print("Help>>然后再到Main>>Youdao>>3:Verificate>>那边进行一个验证可用性")
            print("Help>>这样之后 Words management>>Add中的有道自动填充就可用了")
            print("Help>>并且同时main>>2的翻译也可用了")
            print("Help>>芜湖芜湖！！",end="\n\n")
        if help_sel_main=="2":
            print("Help>>数据库嘛，有4个表")
            print("Help>>分别是youdao,new,prob,fin")
            print("Help>>youdao表里存了1 entry的appid与appsec")
            print("Help>>new和prob表里存了若干entries的CN,EN,value")
            print("Help>>CN代表了中文解释，EN代表英文词条，value代表在Main>>Test>里的成绩")
            print("Help>>这个value基准为0，text每错一次-1,对一次+1")
            print("Help>>fin表里存了Cn,en")
            print("Help>>为什么没有Value？ 你都背熟了还考什么试")
            print("Help>>通过Main>>Migrate也可以发现 fin表只进不出")
            print("Help>>然后在一开始导入数据库的时候 我在下面def了一个db_verification")
            print("Help>>校验表的列是不是足够 符合标准")
            print("Help>>虽然校验的有点草率 但是至少校验了（（（")
            print("Help>>主要依靠数据库提供的功能就是单词存取，测试与迁移（别问为什么没做删除！！没必要！！有这个技术力自己去sqlstudio搞！）")
            print("Help>>看心情再做一个csv导入？")
            print("Help>>这个不一定做，可能会咕咕（",end="\n\n")
            
    if sel=="10":
        db.commit()
        db.close()
        input("Shut>>感谢本次使用. 退出请按回车.")
        break
