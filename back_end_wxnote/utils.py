import sys,os
import django
sys.path.extend([r'/Users/lmq/Downloads/nuxt_vue_django/front_back_end/',])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "front_back_end.settings")
django.setup()

from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from back_end_wxnote.models import note_header
from back_end_wxnote.serializers import note_headerSerializerNew
from back_end_wxnote.models import note_list
from back_end_wxnote.serializers import note_listSerializerNew

import re
htmlf=open('./html/try.html','r',encoding="utf-8")
htmlcont=htmlf.read()
print(type(htmlcont))
import json
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

# ① 首行识别，有"【xxxx】"模式，将整行以下格式输出： "聊天话题：【xxxx】"
kkk0=htmlcont.replace(r'<p>【','聊天话题：【')
kkk00=kkk0.replace(r'】</p>','】\n')
# ②'<p style="font-size: 1.000000em;">Dear:</p>' 仅一个，去掉
kkk1=kkk00.replace(r'<p style="font-size: 1.000000em;">Dear:</p>','\n')   
# ③"<p>&nbsp;</p>" 全去掉
kkk2=kkk1.replace(r'<p>&nbsp;</p>','')
# ④'<p style="text-indent: 2em; font-size: 1.000000em;">' 2021爸爸妈妈联盟&amp;转让 微信群上的聊天记录如下，请查收。"</p>"
#    输出以下格式：邮件标题：2021爸爸妈妈联盟&amp;转让 微信群上的聊天记录如下，请查收。
kkk3=kkk2 .replace(r'<p style="text-indent: 2em; font-size: 1.000000em;">','邮件标题：')
#⑤日期行：
#    <p style="text-align: center; font-size: 1.000000em;"><span style="color: #b8b8b8;">&mdash;&mdash;&mdash;&mdash;&mdash; 2021-03-26 &mdash;&mdash;&mdash;&mdash;&mdash;</span></p>
kkk4=kkk3.replace(r'<p style="text-align: center; font-size: 1.000000em;"><span style="color: #b8b8b8;">&mdash;&mdash;&mdash;&mdash;&mdash;','聊天日期：')
kkk5=kkk4.replace(r'&mdash;&mdash;&mdash;&mdash;&mdash;</span>','')
#⑥去掉无关html格式标注：i、去掉句首<p style="font-size: 1.000000em;"> ;ii、正文句末的</p>全去掉; iii、正文空行，全去掉：<p style="line-height: 1.5em;">&nbsp; iv省略号替换：&hellip;左引号替换：&ldquo; 右引号替换&rdquo;
kkk6=kkk5.replace(r'<p style="font-size: 1.000000em;">','')
kkk7=kkk6.replace(r'</p>','<br>')
kkk8=kkk7.replace(r'<p style="line-height: 1.5em;">&nbsp;','')
kkk9=kkk8.replace(r'&hellip;','...')
kkk9_1=kkk9.replace(r'&ldquo;','“')
kkk9_2=kkk9_1.replace(r'&rdquo;','”')
kkk9_3=kkk9_2.replace(r'<br /><br />','\n')
kkk9_3_1=re.sub(r'<br>','\n',kkk9_3)
kkk9_4=re.sub(r'\n\n','\n',kkk9_3_1)
kkk9_5=re.sub(r'\n\n','\n',kkk9_4)
kkk9_6=re.sub(r'\n\n','\n',kkk9_5)

#开始构建topic表单数据：
print('——————————————————————————————————————————————————')
kk1=r'(聊天话题：【{1}.*?】{1})'
#print(re.findall(kk1, kkk9_6,re.S)[0])
kk1_1=re.findall(kk1, kkk9_6,re.S)[0]
#print(type(kk1_1))
kk2=r'(邮件标题：{1}.*?\n{1})'
#print(re.findall(kk2, kkk9_6,re.S)[0])
kk2_1=re.findall(kk2, kkk9_6,re.S)[0]
#print(type(kk2_1))
kk3=r'(聊天日期：{1}.*?\n{1})'
#print(re.findall(kk3, kkk9_6,re.S))
kk3_1=re.findall(kk3, kkk9_6,re.S)
#print(type(kk3_1))
print(kk3_1)
kk4={}
kk3_1_list=[]

for i in range(len(kk3_1)):
    kk4={"custom_topic":kk1_1,"mail_title":kk2_1[:-2],"date":kk3_1[i][6:-2]}
    #print("date的类型:",type(kk3_1[i][6:16]))
    #print(kk4)
    #存topic
    note_headers_serializer = note_headerSerializerNew(data=kk4)
    data_0 =note_header.objects.filter(custom_topic=kk1_1)
    data_1 = note_header.objects.filter(date=kk3_1[i][6:-2])
    if data_0 and  data_1:
        print("该记录已存在，不存储")
    else:
        # 如果序列化数据有效
        if note_headers_serializer.is_valid():
            print('ok')
            note_headers_serializer.save()
            print("该记录未存在，现已存储")
    #按kk3_1的元素为标准，遍历切割文本
    kk3_1_list.append(kk3_1[i])
    #print('i:',i)
    
print(i,len(kk3_1_list))
goonlist=[]
head=kkk9_6.split(kk3_1_list[0])
#print("head[0]:",head[0])
#print("len(head):",len(head))
goonlist.append(head[0])

#print("goonlist[0]:",goonlist[0])
body=kk3_1_list[0]+head[1]
goonlist.append(body)
#print("goonlist[1]:",goonlist[1])
#print("去掉头部后，开始循环：")

for i in range(1,len(kk3_1_list)+1):
    #print("i:",i)
    #print("kk3_1_list[i-1]:",kk3_1_list[i-1])
    if i<4:
        mm=goonlist[i].split(kk3_1_list[i])
        #去掉了：kk3_1_list[i]
        #print("看一下mm的类型:",type(mm))
        #print("打印一下mm：",mm)
        goonlist[i]=mm[0]
        #print("第",i,"轮goonlist[",i,"]:",goonlist[i])
        #print("看一下mm的长度是：",len(mm))
        
        goonlist.append(kk3_1_list[i]+mm[1])
        #把kk3_1_list[i]补回去，否则下一轮会丢失数据
        #print("goonlist的长度：",len(goonlist))
        #print("————第",i,"轮循环结束————")
    else: 
        print(goonlist[i])
        
print("——————————————这里是goonlist[i],除了goonlist[0]每个都是由日期打头———————————————————")        

kk5={}
print('goonlist共几个：',len(goonlist)) 
#第一个信息goonlist[0]无关，可以抛除
for n in range(1,len(goonlist)):
#for n in range(1,2):
    #print(goonlist[n])
    oo1=r'(<strong>{1}.*?</strong>{1})'
    #print(re.findall(kk1, kkk9_6,re.S)[0])
    oo1_1=re.findall(oo1, goonlist[n],re.S)[0]
    mm=goonlist[n].split("<strong>")
    print("mm用<strong>来做split后，切割出：",len(mm),"条")
    print("进入mm的循环————————————————————————————————")
    
    for o in range(1,len(mm)):
    #for o in range(1,4):
        #第一行mm[0]是日期行
        #print("打印日期行的日期部分：",mm[0][-10:])
        #print("将日期格式化为：YYYY-MM-DD:",'20'+mm[0][-10:])
        aaaaa=('20'+mm[0][-10:])[0:10]
        #print(type(aaaaa))
        date_=datetime.strptime(aaaaa,'%Y-%m-%d')
        print(date_)#xxxx-xx-xx 00:00:00
        #print(type(date_))#<class 'datetime.datetime'>
        #用"/<strong>来且nn"
        #nn是提取出来的：说话人+说话时间、所说内容
        #print("这是第",o,"条(已经去掉第0条：日期行)")
        print("mm[o]切割前",mm[o])
        nn=mm[o].split("</strong>")
        print('29条中，取第',o,'条nn（mm[o]切割后）:',nn)
        print("nn[1]的类型：",type(nn[1]))
        print('29条中，取第',o,'条nn[0]是:',nn[0])
        print('29条中，取第',o,'条nn[1]是:',nn[1])
        
        #talk_time=datetime.strptime(aaaaa+" "+nn[0][-5:]+":00",'%Y-%m-%d %H:%M:%S')
        talk_time=str(aaaaa+" "+nn[0][-5:]+":00")
        
        #print(type(talk_time))
        #print("talk_time:",talk_time)
        chater=nn[0][:-5]
        #print("chater:",chater)
        chat_content=nn[1]
        
        print("chat_content:",chat_content)
        print("chat_content的类型:",type(chat_content))
        #filter返回的是数据库查询，可通用.values('id')活动id值
        #print(note_header.objects.filter(date=date_).values('id'))
        #get获得的是类，type()可看到不同
        #print(note_header.objects.get(date=date_))
        e_note_list_id=note_header.objects.filter(date=date_).values('id')
        print(e_note_list_id[0]['id'])
        ooooooo=note_list.objects.filter(talk_time=talk_time).values('chat_content')
        print("ooooooo是：",ooooooo)
        #当有内容时：
        if len(ooooooo)>0:
            k=[]
            k_ture=[]
            for o in range(len(ooooooo)):
                print("循环前，len(ooooooo)有多大：",len(ooooooo))
                print("☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆☆")
                print("逐个取出ooooooo[o]，准备用来与nn[1]比较，此处是第",o,'个',ooooooo[o])
                kkkoo=ooooooo[o]['chat_content'] #依次取出所有的chat_content
                k.append(kkkoo)
                #print("k是所有append的kkkoo的列表：",k)        
                #未有新存入时
                #如果k中有元素与nn[1]或者nn[1][1:-1]相等就不应该保存
                #并且存入一个true，应清空掉。
                #否则，第二轮时，如果进来一个新元素，因为里面有true,就不会保存了。
                for m in range(len(k)):
                    print("准备ooooooo[o]与nn[1]比较")
                    if nn[1]==k[m] or nn[1][1:-1]==k[m]:
                    #k中有元素与nn[1]或者nn[1][1:-1]相等
                        k_ture.append(True)
                        #每有一个相当，便在k_ture中登记一个true
                        print("看看k_ture有几个：",len(k_ture))
                        print("k_ture分别是啥：",k_ture)
                    #第一轮时，如果k中没有元素与nn[1] or nn[1][1:-1]相等，就应保存nn[1]
                    #但是循环过程中存在一种情况：第一轮出现了True,但是第二轮之后，又出现了新的未保存。
                    #所以应该拿未保存的元素，与k中的所有元素比较，若不存在就应该保存。
                    else:
                        print('nn[1]:',nn[1])
                        print("'chat_content'与nn[1]没有相等，保存nn[1]:")
                        k_ture.append(False)
            if True in k_ture:
                print('nn[1]:',nn[1])
                print ("有True,说明nn[1]已存在，不再存储")
                #如果没有true，就保存一下kk5
            
            else:
                print('nn[1]:',nn[1])
                print("没有发现True，保存nn[1]:")
                kk5={
                    "chat_content":nn[1],
                    "chater":chater,
                    "e_note_list_id":e_note_list_id[0]['id'],
                    "talk_time": talk_time,#json都是文本，没有日期
                }
                note_lists_serializer = note_listSerializerNew(data=kk5)
                if note_lists_serializer.is_valid():
                    print('ok1')
                    note_lists_serializer.save()
                    print("该记录未存在，现已存储1")                 
                    
                    
                    
                    
                                    
        #没有内容时，直接下载：             
        else:
            kk5={
                "chat_content":chat_content,
                "chater":chater,
                "e_note_list_id":e_note_list_id[0]['id'],
                "talk_time": talk_time,#json都是文本，没有日期
            }
            note_lists_serializer = note_listSerializerNew(data=kk5)
            if note_lists_serializer.is_valid():
                print('ok3')
                note_lists_serializer.save()
                print("该记录未存在，现已存储3")   
'''         
    

    
          
       

        
    

    

'''            
#对段落进行结构化提取
#主题


#①按日期切分
#②按<el-checkbox v-model="checked"><strong>切分说人名+时间+聊天内容
#③头部处理
#④尾部处理
#⑤构建模型、api写入数据库




fo = open("./html/try(new-model).html", "w")
fo.write(kkk9_6)
# 关闭文件
fo.close()