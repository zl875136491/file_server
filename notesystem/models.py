from django.db import models
# Create your models here.


class Notes(models.Model):

    title = models.CharField(u"文章标题", max_length=255, unique=True)
    content = models.TextField(u"内容")
    author = models.CharField(max_length=128)
    publish_date = models.DateTimeField(auto_now=True)
    deadline_date = models.CharField(max_length=10)

    def __str__(self):
        return "实验题目：%s  |  实验截止日期：%s" % (self.title, self.deadline_date)

