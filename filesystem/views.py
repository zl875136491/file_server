from django.shortcuts import render
from django import forms
from . import models
from notesystem import models as note_models
import os

# Create your views here.


class FileForm(forms.Form):
    filename = forms.CharField(label="文件名", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    upfile = forms.FileField(label="文件", max_length=128, widget=forms.FileInput(attrs={'class': 'form-control'}))


'''
register函数判断用户的是否为POST请求，如果是并验证是有效的，
然后就返回upload ok!，在验证正确和返回OK的中间放我们的上传文件代码
，因为只有文件上传成功能返回OK
如果是GET请求，就直接显示一个空表单，让用户输入。
'''


def upload(request):
    if request.method == "POST":
        ff = FileForm(request.POST, request.FILES)
        if ff.is_valid():   # 判断是否有效
            # 获取表单元素
            filename = ff.cleaned_data['filename']
            upfile = ff.cleaned_data['upfile']
            # 写入数据库
            file = models.FileModel.objects.create()
            file.file_name = filename
            file.file_path = upfile
            file.file_owner = request.session['user_id']
            file.save()
            return render(request, 'filesystem/uploadok.html')
    else:
        ff = FileForm()
        # 返回一个空表单
    return render(request, 'filesystem/upload.html', {'ff': ff})


def upload2(request):
    all_note = note_models.Notes.objects.all().order_by('publish_date')
    return render(request, 'filesystem/upload2.html', {'list': all_note})

def uploadok(request):

        return render(request, 'filesystem/uploadok.html')


def filemanage(request):
        if request.method == "GET":
            objects = models.FileModel.objects.all()

        return render(request, 'filesystem/filemanage.html', {'list': objects})





