from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse
from . import models

# Create your views here.


class FileForm(forms.Form):
    filename = forms.CharField()
    headImg = forms.FileField()


'''
register函数判断用户的是否为POST请求，如果是并验证是有效的，
然后就返回upload ok!，在验证正确和返回OK的中间放我们的上传文件代码
，因为只有文件上传成功能返回OK
如果是GET请求，就直接显示一个空表单，让用户输入。
'''


def upload(request):
    if request.method == "POST":
        uf = FileForm(request.POST, request.FILES)
        if uf.is_valid():   # 判断是否有效
            # 获取表单元素
            filename = uf.cleaned_data['filename']
            headImg = uf.cleaned_data['headImg']
            # 写入数据库
            file = models.FileModel.objects.create()
            file.file_name = filename
            file.file_path = headImg
            file.save()
            return HttpResponse('upload ok!')
    else:
        uf = FileForm()
        # 返回一个空表单
    return render(request, 'filesystem/upload.html', {'uf': uf})
