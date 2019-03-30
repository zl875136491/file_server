from django.shortcuts import render,render_to_response
from django import forms
from django.http import HttpResponse
from . import models
from django.contrib.auth.decorators import login_required
# Create your views here.


class FileForm(forms.Form):
    filename = forms.CharField(label="文件名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    headImg = forms.FileField(label="文件", max_length=128, widget=forms.FileInput(attrs={'class': 'form-control'}))


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
            return render(request, 'filesystem/uploadok.html')
    else:
        uf = FileForm()
        # 返回一个空表单
    return render(request, 'filesystem/upload.html', {'uf': uf})


def uploadok(request):
    pass
    # TODO: 验证文件是否上传
    return render(request, 'filesystem/uploadok.html')


def filemanage(request):
    pass
    # TODO：显示文件
    return render(request, 'filesystem/filemanage.html')


def noteediter(request):
    pass
    return render(request, 'filesystem/noteediter.html')


def notereciver(request):
    pass
    return render(request, 'filesystem/notereciver.html')
