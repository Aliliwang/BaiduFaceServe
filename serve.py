import base64
import os
import socket
import re
from aip import AipFace
from sql import SQL


APP_ID = '17694061'
API_KEY = 'qpf2Xas6RUXVEMiCuUzDQsLX'
SECRET_KEY = 'id5eDhsoK2IY8jSMoEKrtpqm9kGwIfFH'
client = AipFace(APP_ID, API_KEY, SECRET_KEY)
groupId = "user"
imageType="BASE64"


serve=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
serve.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
host='172.16.186.72'
port=9527
serve.bind((host,port))
serve.listen(5)
sql=SQL()
while True:
    connect,addr=serve.accept()
    while True:
        data = connect.recv(1024).decode()
        results=re.split('#',data)
        if results[0]=='log':
            if  results[1]==sql.findname(results[1]) and results[2]==sql.findpwd(results[1]):
                print('correct')
                connect.send(('correct').encode('utf-8'))
            else:
                print('error')
                connect.send(('error').encode('utf-8'))
        elif results[0]=='reg':
            if  sql.regist(results[1],results[2])=='pass':
                print("pass")
                connect.send(('pass').encode('utf-8'))
            else:
                print("exist")
                connect.send(('error').encode('utf-8'))
        elif results[0]=='upload':
                 print(data)
                 name=results[1]
                 image=b''

                 while True:
                     datas=connect.recv(40960000)
                     image+=datas
                     if len(datas)==0:
                         break

                 image64=base64.b64encode(image)
                 string = str(image64, 'utf-8')
                 get = client.addUser(string, imageType, groupId, name)
                 print(get['error_msg'])

                 filename = os.path.join('/image/', name)
                 fp = open(filename, 'wb')
                 fp.write(image)
                 fp.close()

        elif results[0]=='single':
                 print(data)
                 image = b''

                 while True:
                     datas = connect.recv(40960000)
                     image += datas
                     if len(datas) == 0:
                          break

                 image64 = base64.b64encode(image)
                 string = str(image64, 'utf-8')
                 get = client.search(string,imageType,groupId)
                 if get["error_msg"] in "SUCCESS":
                         score = get["result"]["user_list"][0]["score"]
                         name = get["result"]["user_list"][0]["user_id"]
                         print(name,score)
                         if score>80:
                             connect.send((name).encode('utf-8'))
                         else:
                             print("查无此人")
                             connect.send(("查无此人").encode('utf-8'))

                 else:
                         print("查无此人")
                         connect.send(("查无此人").encode('utf-8'))



        elif results[0]=='mutiply':
                print(data)
                image = b''

                while True:
                         datas = connect.recv(40960000)
                         image += datas
                         if len(datas) == 0:
                               break
                image64 = base64.b64encode(image)
                string = str(image64, 'utf-8')
                options={}
                options["max_face_num"] =10
                get = client.multiSearch(string, imageType, groupId,options)
                print(get['error_msg'])
                if get["error_msg"] in "SUCCESS":
                      total= len(get["result"]["face_list"])
                      num=0
                      list=[]
                      for j in range(total):
                            if len(get["result"]["face_list"][j]["user_list"])!=0:
                                list.append(j)
                                num+=1
                      print(num)
                      st=''
                      for i in range(num):
                           top=get["result"]["face_list"][list[i]]["location"]["top"]
                           left=get["result"]["face_list"][list[i]]["location"]["left"]
                           name=get["result"]["face_list"][list[i]]["user_list"][0]["user_id"]
                           print(name,left,top)
                           st+=name+'#'+str(left)+'#'+str(top)+'#'
                      print(st)
                      connect.send((st).encode('utf-8'))
                else:
                     print("查无结果")
                     connect.send(("error").encode('utf-8'))
        elif results[0]=='pk':
                print(data)
                image = b''

                while True:
                    datas = connect.recv(40960000)
                    image += datas
                    if len(datas) == 0:
                        break
                image64 = base64.b64encode(image)
                string = str(image64, 'utf-8')
                options = {}
                options["face_field"]="beauty"
                echo=client.detect(string, imageType, options)
                beauty=echo["result"]["face_list"][0]["beauty"]
                get = client.search(string, imageType, groupId)
                if get["error_msg"] in "SUCCESS":
                    name = get["result"]["user_list"][0]["user_id"]
                    score =round(get["result"]["user_list"][0]["score"],2)
                    st=''

                    path="/image/"+name
                    file= open(path, 'rb')
                    bytes=file.read()
                    size=len(bytes)
                    st = str(beauty) + '#' + name + '#' + str(score) + '%#' + str(size)
                    print(st)
                    connect.send((st).encode('utf-8'))

                else:
                    print("无图像")
                    connect.send(("error").encode('utf-8'))
        elif results[0]=='image':
                print(data)
                name=results[1]
                path = "/image/" + name
                file = open(path, 'rb')
                bytes = file.read()
                connect.sendall(bytes)
                print("image success")






        connect.close()
        break


