import requests
import re
import json
import random
import time
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
           'Content-Type': 'application/json'}
a="不错嘛，必须三连！"
dianguo=[]
emoji_list=[
    "编程猫_666",
    "编程猫_棒",
    "编程猫_打call",
    "编程猫_爱心",
    "编程猫_我来啦",
    "雷电猴_哇塞",
    "雷电猴_围观",
    "魔术喵_魔术",
    "魔术喵_点赞",
    "魔术喵_开心",
    "星能猫_耶"
]
def qingqiu(name,url,data,cookie,ma):
    return_post=requests.post(url=url,data=data,headers=headers,cookies=cookie)
    if return_post.status_code==ma:
        print('----'+name+' is right----')
    else:
        print('----'+name+'_worry:{}----'.format(str(return_post.status_code)))
def main():
    name=input("账号:")
    password=input("密码:")
    url_denglu="https://api.codemao.cn/tiger/v3/web/accounts/login"
    data = json.dumps({"identity": name, "password": password, "pid": '65edCTyg'})
    return_denglu = requests.post(url=url_denglu, data=data, headers=headers)
    if return_denglu.status_code==200:
        print('----Loading......----')
        cookie=return_denglu.cookies
        while True:
            print('It has caught 200 new works.')
            new_works=""
            url='https://api.codemao.cn/creation-tools/v1/pc/discover/newest-work?work_origin_type=ORIGINAL_WORK&offset=0&limit=200'
            new_works=requests.get(url=url,headers=headers)
            work_name_list=re.findall('\"work_name\":\"(.*?)\",',new_works.text)
            user_name_list=re.findall('\"nickname\":\"(.*?)\",',new_works.text)
            user_id_list=re.findall('\"user_id\":(.*?),',new_works.text)
            work_id_list=re.findall('\"work_id\":(.*?),',new_works.text)
            start=time.time()
            for work_name,user_name,user_id,work_id,num in zip(work_name_list,user_name_list,user_id_list,work_id_list,range(1,1001)):
                print('number:{}\n{}\n{}\n{}\n{}'.format(num,user_name,user_id,work_name,work_id))
                if work_id not in dianguo:
                    em=random.choice(emoji_list)
                    qingqiu('DZ','https://api.codemao.cn/nemo/v2/works/{}/like'.format(work_id),{},cookie,200)
                    qingqiu('SC','https://api.codemao.cn/nemo/v2/works/{}/collection'.format(work_id),{},cookie,200)
                    qingqiu('GZ','https://api.codemao.cn/nemo/v2/user/{}/follow'.format(user_id),{},cookie,204)
                    end=time.time()
                    if int(end-start)>=12:
                        qingqiu('PL','https://api.codemao.cn/creation-tools/v1/works/{}/comment'.format(work_id),json.dumps({"emoji_content": em, "content": a}),cookie,201)
                        start=time.time()
                    dianguo.append(work_id)
                    time.sleep(1)
                else:
                    print('----FULI has been----')
            huida=input('<Y to next and other to quit>')
            if huida!='Y':
                print('----Goobye!----')
                break
    else:
        print('----Worry:{}----'.format(str(return_denglu.status_code)))
if __name__ == "__main__":
    main()