import pymysql
class SQL:
     def __init__(self):
        self.db = pymysql.connect(host='127.0.0.1', user="root", passwd="199312", db="user", port=3306, charset="utf8")

     def regist(self,str1,str2):
        sql="insert into log(account,pwd)values('%s','%s')"%(str1,str2)
        cur=self.db.cursor()
        try:
            cur.execute(sql)
            self.db.commit()
        except BaseException:
            return "exist"
        else:
            return "pass"

     def findname(self,str):
        sql="select account from log where account='%s'"%str
        cur=self.db.cursor()
        cur.execute(sql)
        results=cur.fetchall()
        if results:
            return results[0][0]
        else:
            return "null"


     def findpwd(self, str):
        sql="select pwd from log where account='%s'"%str
        cur=self.db.cursor()
        cur.execute(sql)
        results=cur.fetchall()
        if results:
            return results[0][0]
        else:
            return "null"


