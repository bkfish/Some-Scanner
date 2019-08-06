import threading
import time
import os
import re
import requests
from queue import Queue
file_count = 0
url = "http://127.0.0.1"

url_list=[] #存储名字名称列表
nameSepList=[] #存储分分离后的文件名称列表
#把文件名存储起来 过滤拿到我们想要的文件后缀
threadLock = threading.Lock()
base_dir='E:/CodingSoftware/PhpStudy/PHPTutorial/WWW'
print("base_url: "+url)
print("base_dir: "+base_dir)

def get_url_list():
    base_url=url
    work_dir = base_dir
    length=len(work_dir)
    for parent, dirnames, filenames in os.walk(work_dir,  followlinks=True):
        for filename in filenames:
            file_path = os.path.join(parent, filename)
            #print('文件名：%s' % filename)
            file_path1=file_path[length:]
            file_path2=file_path1.replace('\\','/')
            if file_path2.endswith('.php') and  ('phpMyAdmin' not in file_path2):
                url_list.append(base_url+file_path2)
                #print(base_url+file_path2)
#每个线程的运作 参数为文件名称的列表
def run(name_list):
    for k in name_list:
        #print(k)
        obj_path=k[len(url):]
        file_path=base_dir+obj_path
        try:
            with open(file_path, 'rt', errors='ignore') as f:
                content = f.read()
                get = re.findall(r"GET\['([A-Za-z_-]+?)'\]", content)
                get1 = re.findall(r"GET\[\"([A-Za-z_-]+?)\"\]", content)
                get2 = re.findall(r"GET\[([A-Za-z_-]+?)\]", content)
                post = re.findall(r"POST\['([A-Za-z_-]+?)'\]", content)
                post1 = re.findall(r"POST\[\"([A-Za-z_-]+?)\"\]", content)
                post2 = re.findall(r"POST\[([A-Za-z_-]+?)\]", content)
                for i in get:
                    get_rep(k,i)
                    print(obj_path+" Key is: "+i)
                for i in get1:
                    get_rep(k,i)
                    print(obj_path+" Key is: "+i)
                for i in get2:
                    get_rep(k,i)
                    print(obj_path+" Key is: "+i)
                for i in post:
                    post_rep(k,i)
                    print(obj_path+" Key is: "+i)
                for i in post1:
                    post_rep(k,i)
                    print(obj_path+" Key is: "+i)
                for i in post2:
                    post_rep(k,i)
                    print(obj_path+" Key is: "+i)
                f.close()
        except Exception as e:
            raise e
#做GET请求
def get_rep(base_url, name):
    r_url = base_url +  "?" + str(name) + "=echo 'Hello Kitty';"
    #print(r_url)
    rep = requests.get(r_url)
    if 'Hello Kitty' in rep.content.decode('gbk'):
        Record_To_File(r_url,name)

def post_rep(base_url, name):

    r_url = base_url 
    param = {
        name: "echo 'HelloKitty';"
    }
    rep = requests.post(r_url, data=param)
    #print(r_url + " POST: " + name)
    if 'HelloKitty' in rep.content.decode('gbk'):
        Record_To_File(r_url,name)


def Record_To_File(filename,name):
    answer = open('answer.txt','a+')
    end = time.time()
    answer.write("Got It!   !!!!!!! " + filename + " The param is: [\'" + name +"\']\n")
    print("Got It!   !!!!!!! " + filename + " The param is: [\'" + name +"\']")
    answer.close()


if __name__=='__main__':
    get_url_list()
    run(url_list)
