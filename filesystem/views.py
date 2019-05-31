from django.shortcuts import render
from . import models
from notesystem import models as note_models
import os, time, zipfile, shutil, string, random
from django.http import StreamingHttpResponse


def upload(request):
    all_note = note_models.Notes.objects.all().order_by('publish_date')
    if request.method == "POST":
        attribution = request.POST.get('file_attribution')
        cleaned_attribution = str(attribution).split('|')[0].rstrip()
        clear_title = cleaned_attribution.split('：')[1].rstrip()
        report_id = note_models.Notes.objects.get(title=clear_title).id
        ownerid = request.session['user_id']
        name = str(request.session['user_id']) + '-' + str(report_id)
        up_file = request.FILES.get('upload_file', None)
        if not attribution:
            message = "所选章节错误"
            return render(request, 'filesystem/upload.html', {'list': all_note}, locals())
        if models.FileModel.objects.filter(file_name=name):
            message = "你已经交过报告了，请勿重复提交！"
            return render(request, 'filesystem/uploadok.html', locals())
        else:
            try:
                path = os.path.join('media', up_file.name)
                storage = open(path, 'wb+')  # 打开存储文件
                for chunk in up_file.chunks():  # 分块写入文件
                    storage.write(chunk)
                storage.close()
            except Exception as e:
                message = '文件状态错误！'
                return render(request, 'filesystem/upload.html', locals())
            file = models.FileModel.objects.create()
            file.file_name = name
            file.file_owner = ownerid
            file.file_path = path
            file.file_attribution = cleaned_attribution.split('：')[1]
            file.save()
            message = "上传成功!"
            return render(request, 'filesystem/uploadok.html', locals())
    else:
        return render(request, 'filesystem/upload.html', {'list': all_note})


def uploadok(request):
        pass
        return render(request, 'filesystem/uploadok.html')


def filemanage(request):
        if request.method == "POST":
            file_id_list = request.POST.getlist('test', '')
            file_path_list = []
            for i in file_id_list:
                file_path_list.append(str(models.FileModel.objects.get(id=i).file_path))

            downloader_name = request.session['user_id']
            time_str = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))

            zip_path_name = str(downloader_name) + '-' + time_str + '-' + ran_str
            zip_name = zip_path_name + '.zip'

            os.mkdir(zip_path_name)
            for p in file_path_list:                                # 复制选中文件到归档目录
                shutil.copy(p, zip_path_name)
            zip_dir(zip_path_name, zip_name)                        # 压缩函数
            shutil.move(zip_name, 'media')
            shutil.rmtree(zip_path_name)
            response = StreamingHttpResponse(readFile('media\\'+zip_name))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(zip_name)
            return response

        if request.method == "GET":
            objects = models.FileModel.objects.all()
            return render(request, 'filesystem/filemanage.html', {'list': objects})


def readFile(filename, chunk_size=512):
    """下载文件函数"""
    with open(filename, 'rb') as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def zip_dir(dirname,zipfilename):
    """ 压缩函数"""
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else:
        for root, dirs, files in os.walk(dirname):
            for dir in dirs:
                filelist.append(os.path.join(root, dir))
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        zf.write(tar, arcname)
    zf.close()


