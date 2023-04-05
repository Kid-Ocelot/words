'''
db = sqlite3.connect("test.db")
db.execute("")
CREATE TABLE tbl (line1 INTEGER PRIMARY KEY,line2 TEXT,line3 TEXT)
INSERT INTO tbl (line1,line2,line3) values (1,test,114514fish)
UPDATE tbl SET line2="1919810Kid" WHERE line1="1"

https://www.w3school.com.cn/python/python_try_except.asp

print("Conn>>Created Words.db",end="\n\n")

youdao_return=youdaoRequest("apple","2827c6145da76315","K73llfrGOr7h4tlK9lbHJsxojaRpSIE4","zh-CHS")#zh-CHS/en
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

def connect_db(db_input):
    if db_input == "empty":
        db=sqlite3.connect("Words.db")
        db.execute("CREATE TABLE youdao (appID TEXT,appSECRET TEXT,access INTEGER)")
        db.execute("CREATE TABLE new (CN TEXT,EN TEXT,CN2EN INTEGER DEFAULT(0),EN2CN INTEGER DEFAULT(0))")
        db.execute("CREATE TABLE prob (CN TEXT,EN TEXT,CN2EN INTEGER DEFAULT(0),EN2CN INTEGER DEFAULT(0))")
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
        print("Veri>>Table youdao error")
        errors=errors+1
    try:
        db.execute("SELECT CN,EN,CN2EN,EN2CN from new")
    except sqlite3.OperationalError:
        print("Veri>>Table new error")
        errors=errors+1
    try:
        db.execute("SELECT CN,EN,CN2EN,EN2CN from prob")
    except sqlite3.OperationalError:
        print("Veri>>Table prob error")
        errors=errors+1
    try:
        db.execute("SELECT CN,EN from fin")
    except sqlite3.OperationalError:
        print("Veri>>Table fin error")
        errors=errors+1
    print("Veri>>Found",errors,"error(s).")
    if errors>0:
        print("Veri>>",errors,"found,consider creating a new database.",end="\n\n")
    else:
        print("Veri>>Verification passed.",end="\n\n")

def mainChoice():
    print("Main>>Choose operation.")
    print("Main>>1:Configure youdao-id")
    print("Main>>2:Translate a given word")
    print("Main>>3:Words Management")
    print("Main>>4")
    print("Main>>5")
    print("Main>>6")
    print("Main>>7")
    print("Main>>8")
    print("Main>>9")
    print("Main>>10:Close the DB")
    sel=str(input("Main>>Operation id:"))
    return sel

def youdaoGlobalinfoRefresh():
    youdao_appID=db.execute("Select appID from youdao").fetchone()[0]
    youdao_appSECRET=db.execute("Select appSECRET from youdao").fetchone()[0]
    return youdao_appID,youdao_appSECRET

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
#################################################youdao-request
print("""
Author>>Word Automatic translation and testing System
Author>>Written by Kid-Ocelot
Author>>Requires Verificated Youdao-app to have best experience
""")

db_int_sel=str(input("Conn>>1:Connect;2.Create:"))
if db_int_sel=="1":
    #db=connect_db(str(input("Name of db:")))
    db=connect_db("Words.db")#Fast testment,Changing later
else:
    db=connect_db("empty")
    print("Conn>>Created Words.db",end="\n\n")
print("Veri>>Database connected,verificating it.")
db_verification(db)

#During the main Program, Don't forget to db.commit()!

while True:
    youdao_veri=0
    youdao_res_veri1=db.execute("Select appID from youdao").fetchone()[0]
    youdao_res_veri2=db.execute("Select appSECRET from youdao").fetchone()[0]
    if youdao_res_veri1 == None or youdao_res_veri2 == None:
        print("Main>>Appid/Appsecret not found.",end="\n\n")
        youdao_veri=1
    else:
        #Refresh app algorithm
        youdao_appID=youdaoGlobalinfoRefresh()[0]
        youdao_appSECRET=youdaoGlobalinfoRefresh()[1]
        if db.execute("SELECT access from youdao").fetchone()[0]!=1:
            print("Main>>Youdao Info found but not verificated.",end="\n\n")
    sel=mainChoice()
    print()#\n
    if sel=="1":#Youdao id Config
        youdao_sel_main=str(input("Youdao>>1:Input new info.2:Show current info.3.Verificate current info. Choice:"))
        if youdao_sel_main=="1":
            print("Youdao>>Now inputing new info.")
            youdao_res_appID=str(input("Youdao>>appID:"))
            youdao_res_appSECRET=str(input("Youdao>>appSECRET:"))
            if youdao_veri!=1:
                print("Youdao>>Cleared current info.")
                db.execute("Delete from youdao")
            db.execute("Insert into youdao (appID,appSECRET) values ('"+youdao_res_appID+"','"+youdao_res_appSECRET+"')")
            db.execute("UPDATE youdao SET access=0")
            print("Youdao>>Sucessfully inserted the new info.",end="\n\n")
            db.commit()
        if youdao_sel_main=="2":
            print("Youdao>>Now checking info.")
            if youdao_veri==1:
                print("Youdao>>Infomation missing.")
            youdao_check_appid=db.execute("Select appID from youdao").fetchone()
            youdao_check_appsec=db.execute("Select appSECRET from youdao").fetchone()
            youdao_check_appaccess=db.execute("SELECT access from youdao").fetchone()
            if youdao_check_appaccess[0]==1:
                youdao_check_appaccess="True"
            else:
                youdao_check_appaccess="False"
            print("Youdao>>appID:",youdao_check_appid[0])
            print("Youdao>>appSECRET:",youdao_check_appsec[0])
            print("Youdao>>Accessbility:",youdao_check_appaccess)
            print("Youdao>>Sucessfully shown the current info.",end="\n\n")
        if youdao_sel_main=="3":
            print("Youdao>>Now verificating app accessbility.")
            if youdao_veri==1:
                print("Youdao>>Appid/Appsecret missing.")
            if youdao_veri==0:
                try:
                    youdao_accessbility=youdaoRequest("apple",youdao_appID,youdao_appSECRET,"zh-CHS")#zh-CHS/en
                except:
                    print("Youdao>>Accessbility test not passed.",end="\n\n")
                    youdao_accessbility=("error")
                if youdao_accessbility[1]=="0":
                    print("Youdao>>Accessbility test passed.",end="\n\n")
                    db.execute("UPDATE youdao SET access=1")
                    db.commit()
    if sel=="2":#Translation
        trans_veri_access=db.execute("Select access from youdao").fetchone()[0]
        if trans_veri_access!=1:
            print("Trans>>Please first pass the accessbility check in the Youdao-id>>Verificate")
        else:
            trans_type_sel=str(input("Trans>>Select destination language: 1:English 2:Chinese:"))
            trans_query=str(input("Trans>>Input Beginning String:"))
            if trans_type_sel != "2":
                trans_type_sel="en"
            else:
                trans_type_sel="zh-CHS"
            print("Trans>>",str(youdaoRequest(trans_query,youdao_appID,youdao_appSECRET,trans_type_sel)[0]),end="\n\n")
    if sel=="3":#Manage Words
        mana_sel_main=str(input("Manage>>1:Input New Word 2:View current tables :"))
        if mana_sel_main=="1":
            print("Manage>>Input Method only allows Table new,for further management use SQliteStudio.")
            #mana>>inp>>Selecion matrix

            #Check accessbility
            if db.execute("SELECT access from youdao").fetchone()[0]==1:
                mana_sel_Input_youdao=str(input("Manage>>Input>>Select youdao auto-fill requirement 1:Automatic 2:Manual:"))
            else:
                mana_sel_Input_youdao="2"
            mana_sel_Input_method=str(input("Manage>>Input>>Select Input Method 1:Single 2:Multple(Insert Nothing/ENTER to exit)"))
            #Once AutoYoudao isn't chosen,Input Preference==CN
            #a.k.a "212" & "222" choices can't be chosen
            #Down there "122" "222" can't be chosen
            #Down there "212"&"222" are the same

            if mana_sel_Input_youdao=="1":
                mana_sel_Input_preference=str(input("Manage>>Input>>Select First Insert Character 1:CN 2:EN:"))
            else:
                mana_sel_Input_preference="1"

            mana_char_en=""
            mana_char_cn=""
            mana_count=0
            if mana_sel_Input_method=="1" and mana_sel_Input_preference=="1" and mana_sel_Input_youdao=="1":
                mana_char_cn=str(input("Manage>>Input>>Insert CN character"))
                mana_char_en=str(youdaoRequest(mana_char_cn,youdao_appID,youdao_appSECRET,"en")[0])
                db.execute("Insert into new(CN,EN) values('"+mana_char_cn+"','"+mana_char_en+"')")
                print("Manage>>Input>>Successfully Inserted  "+mana_char_cn+" , "+mana_char_en)
            if mana_sel_Input_method=="1" and mana_sel_Input_preference=="1" and mana_sel_Input_youdao=="2": #same as 222
                mana_char_cn=str(input("Manage>>Input>>Insert CN character"))
                mana_char_en=str(input("Manage>>Input>>Insert EN character"))
                db.execute("Insert into new(CN,EN) values('"+mana_char_cn+"','"+mana_char_en+"')")
                print("Manage>>Input>>Successfully Inserted  "+mana_char_cn+" , "+mana_char_en,end="\n\n")
            if mana_sel_Input_method=="1" and mana_sel_Input_preference=="2" and mana_sel_Input_youdao=="1":
                mana_char_en=str(input("Manage>>Input>>Insert EN character"))
                mana_char_cn=str(youdaoRequest(mana_char_en,youdao_appID,youdao_appSECRET,"zh-CHS")[0])
                db.execute("Insert into new(CN,EN) values('"+mana_char_cn+"','"+mana_char_en+"')")
                print("Manage>>Input>>Successfully Inserted  "+mana_char_cn+" , "+mana_char_en,end="\n\n")
            if mana_sel_Input_method=="1" and mana_sel_Input_preference=="2" and mana_sel_Input_youdao=="2": #same as 212 #Can't be chosen
                mana_char_cn=str(input("Manage>>Input>>Insert CN character"))
                mana_char_en=str(input("Manage>>Input>>Insert EN character"))
                db.execute("Insert into new(CN,EN) values('"+mana_char_cn+"','"+mana_char_en+"')")
                print("Manage>>Input>>Successfully Inserted  "+mana_char_cn+" , "+mana_char_en,end="\n\n")
            if mana_sel_Input_method=="2" and mana_sel_Input_preference=="1" and mana_sel_Input_youdao=="1":#cn2en
                mana_count=0
                while True:
                    mana_char_cn=str(input("Manage>>Input>>Insert CN character"))
                    if mana_char_cn=="":
                        print("Manage>>Input>>Exited inputing mode with "+str(mana_count)+" word(s) inserted.",end="/n/n")
                        break
                    else:
                        mana_char_en=str(youdaoRequest(mana_char_cn,youdao_appID,youdao_appSECRET,"en")[0])
                        db.execute("Insert into new(CN,EN) values('"+mana_char_cn+"','"+mana_char_en+"')")
                        print("Manage>>Input>>Successfully Inserted  "+mana_char_cn+" , "+mana_char_en,end="\n\n")
                        mana_count=mana_count+1
            if mana_sel_Input_method=="2" and mana_sel_Input_preference=="1" and mana_sel_Input_youdao=="2":#Same as 122
                mana_count=0
                while True:
                    mana_char_cn=str(input("Manage>>Input>>Insert CN character"))
                    mana_char_en=str(input("Manage>>Input>>Insert EN character"))
                    if mana_char_cn=="" or mana_char_en=="":
                        print("Manage>>Input>>Exited inputing mode with "+str(mana_count)+" word(s) inserted.",end="/n/n")
                        break
                    else:
                        db.execute("Insert into new(CN,EN) values('"+mana_char_cn+"','"+mana_char_en+"')")#en2cn
                        print("Manage>>Input>>Successfully Inserted  "+mana_char_cn+" , "+mana_char_en,end="\n\n")
                        mana_count=mana_count+1
            if mana_sel_Input_method=="2" and mana_sel_Input_preference=="2" and mana_sel_Input_youdao=="1":
                mana_count=0
                while True:
                    mana_char_en=str(input("Manage>>Input>>Insert EN character"))
                    if mana_char_en=="":
                        print("Manage>>Input>>Exited inputing mode with "+str(mana_count)+" word(s) inserted.",end="/n/n")
                        break
                    else:
                        mana_char_cn=str(youdaoRequest(mana_char_en,youdao_appID,youdao_appSECRET,"zh-CHS")[0])
                        db.execute("Insert into new(CN,EN) values('"+mana_char_cn+"','"+mana_char_en+"')")
                        print("Manage>>Input>>Successfully Inserted  "+mana_char_cn+" , "+mana_char_en,end="\n\n")
                        mana_count=mana_count+1
                if mana_sel_Input_method=="2" and mana_sel_Input_preference=="2" and mana_sel_Input_youdao=="2":#Same as 112 Can't be chosen
                    mana_count=0
                    while True:
                        mana_char_cn=str(input("Manage>>Input>>Insert CN character"))
                        mana_char_en=str(input("Manage>>Input>>Insert EN character"))
                        if mana_char_cn=="" or mana_char_en=="":
                            print("Manage>>Input>>Exited inputing mode with "+str(mana_count)+" word(s) inserted.",end="/n/n")
                            break
                        else:
                            db.execute("Insert into new(CN,EN) values('"+mana_char_cn+"','"+mana_char_en+"')")
                            print("Manage>>Input>>Successfully Inserted  "+mana_char_cn+" , "+mana_char_en,end="\n\n")
                            mana_count=mana_count+1
            db.commit()
        if mana_sel_main=="2":#View tables
            mana_view_tuple=db.execute("SELECT CN,EN from new").fetchall()#new
            #递归-Recursion
            mana_recur_int=0
            while True:
                try:
                    mana_view_tuple[mana_recur_int]
                    mana_recur_int=mana_recur_int+1
                except:
                    break
            print("Manage>>View>>",mana_recur_int,"word(s) found in Table new.")
            for i in range(0,mana_recur_int,1):
                print("Manage>>View>>Table new: CN:",mana_view_tuple[i][0],", EN:",mana_view_tuple[i][1])
            print()#\n

            mana_view_tuple=db.execute("SELECT CN,EN from prob").fetchall()#prob
            #递归-Recursion
            mana_recur_int=0
            while True:
                try:
                    mana_view_tuple[mana_recur_int]
                    mana_recur_int=mana_recur_int+1
                except:
                    break
            print("Manage>>View>>",mana_recur_int,"word(s) found in Table prob.")
            for i in range(0,mana_recur_int,1):
                print("Manage>>View>>Table new: CN:",mana_view_tuple[i][0],", EN:",mana_view_tuple[i][1])
            print()#\n

            mana_view_tuple=db.execute("SELECT CN,EN from fin").fetchall()#fin
            #递归-Recursion
            mana_recur_int=0
            while True:
                try:
                    mana_view_tuple[mana_recur_int]
                    mana_recur_int=mana_recur_int+1
                except:
                    break
            print("Manage>>View>>",mana_recur_int,"word(s) found in Table fin.")
            for i in range(0,mana_recur_int,1):
                print("Manage>>View>>Table new: CN:",mana_view_tuple[i][0],", EN:",mana_view_tuple[i][1])
            print()#\n
    if sel=="10":
        db.commit()
        db.close()
        input("Shut>>Thanks for using! Press ENTER to exit.")
        break
