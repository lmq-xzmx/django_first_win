from django.db import models

# Create your models here.
class note_header(models.Model):
    # 聊天话题
    # 邮件标题
    # 聊天日期
    custom_topic = models.CharField(verbose_name='聊天话题',max_length=64)
    mail_title = models.CharField(verbose_name='邮件标题',max_length=64)
    date = models.DateField(verbose_name='聊天日期')
    created = models.DateTimeField(verbose_name='创建时间',auto_now_add=True,blank=True)
    
    #改写类中的__str__方法后可以在print时得到想要的易于人阅读的对象的信息
    def __str__(self):
        return self.custom_topic
    #
    class Meta:
        db_table = 'note_header'
        #verbose_name指定在admin管理界面中显示中文；
        #verbose_name表示单数形式的显示，
        #verbose_name_plural表示复数形式的显示；中文的单数和复数一般不作区别。
        verbose_name = '聊天记录基本信息'
        verbose_name_plural = verbose_name

class note_list(models.Model):
    #聊天日期时间
    #说话者
    #聊天内容
    talk_time  = models.DateTimeField(verbose_name='聊天时间') 
    chater = models.CharField(verbose_name='说话人',max_length=32)
    chat_content = models.TextField(verbose_name='聊天内容')
    created = models.DateTimeField(verbose_name='创建时间',auto_now_add=True,blank=True)
    #聊天外键
    e_note_list = models.ForeignKey(note_header,on_delete=models.CASCADE)
    
    def __str__(self):
        return 'id为：'+str(self.id)+'的对象'
    class Meta:
        db_table = 'note_list'
        verbose_name = '聊天内容列表'
        verbose_name_plural = verbose_name

#原文链接：https://blog.csdn.net/weixin_43229819/article/details/102941350