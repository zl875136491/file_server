from django.shortcuts import render
from django import forms
from . import models
from notesystem import models as note_models
import os

# Create your views here.



'''
register函数判断用户的是否为POST请求，如果是并验证是有效的，
然后就返回upload ok!，在验证正确和返回OK的中间放我们的上传文件代码
，因为只有文件上传成功能返回OK
如果是GET请求，就直接显示一个空表单，让用户输入。
'''


def upload(request):
    all_note = note_models.Notes.objects.all().order_by('publish_date')
    if request.method == "POST":
        attribution = request.POST.get('file_attribution')
        cleaned_attribution = str(attribution).split('|')[0].rstrip()
        owner = request.session['user_id']
        name = str(request.session['user_id']) + '-' + cleaned_attribution
        up_file = request.FILES.get('upload_file', None)

        if not attribution:
            message = "attribution error!"
            return render(request, 'filesystem/upload.html', {'list': all_note}, locals())

        else:
            try:
                path = os.path.join('media', up_file.name)
                storage = open(path, 'wb+')  # 打开存储文件
                for chunk in up_file.chunks():  # 分块写入文件
                    storage.write(chunk)
                storage.close()
            except Exception as e:
                message = 'file error'
                return render(request, 'filesystem/upload.html', locals())
            file = models.FileModel.objects.create()
            file.file_name = name
            file.file_owner = owner
            file.file_path = path
            file.file_attribution = cleaned_attribution.split('：')[1]
            file.save()
            message = "Successful!"
            return render(request, 'filesystem/uploadok.html', locals())
    else:
        return render(request, 'filesystem/upload.html', {'list': all_note})


def uploadok(request):
        pass
        return render(request, 'filesystem/uploadok.html')


def filemanage(request):
        if request.method == "GET":
            objects = models.FileModel.objects.all()

        return render(request, 'filesystem/filemanage.html', {'list': objects})





