from django.shortcuts import render
from . import models
from notesystem import models as note_models
from django.http import StreamingHttpResponse
import os, time, zipfile, shutil, string, random, datetime


def upload(request):
    # 获取当天时间并格式化
    time_sys = str(datetime.datetime.now()).split(' ')[0]
    print(time_sys)
    year_sys, month_sys, day_sys = time_sys.split('-')
    time_today = str(year_sys) + str(month_sys) + str(day_sys)
    all_note = note_models.Notes.objects.filter(deadline_date__gte=time_today)
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
        # 文件保存
        else:
            try:
                path = os.path.join('media', up_file.name)
                storage = open(path, 'wb+')  # 打开存储文件
                for chunk in up_file.chunks():  # 分块写入文件
                    storage.write(chunk)
                storage.close()
                os.rename(path, name+'.doc')
                shutil.move(name+'.doc', 'media')
            except Exception as e:
                message = '文件状态错误！'
                return render(request, 'filesystem/upload.html', locals())
            file = models.FileModel.objects.create()
            file.file_name = name
            file.file_owner = ownerid
            file.file_path = 'media\\' + name + '.doc'
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
            # 构造数据项
            downloader_name = request.session['user_id']
            time_str = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 8))
            # 使用数据项为zip文件命名
            zip_path_name = str(downloader_name) + '-' + time_str + '-' + ran_str
            zip_name = zip_path_name + '.zip'
            # 复制选中文件到归档目录
            os.mkdir(zip_path_name)
            for p in file_path_list:
                shutil.copy(p, zip_path_name)
            zip_dir(zip_path_name, zip_name)
            shutil.move(zip_name, 'media')
            shutil.rmtree(zip_path_name)
            response = StreamingHttpResponse(readFile('media\\'+zip_name))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(zip_name)
            return response

        if request.method == "GET":
            objects = models.FileModel.objects.all()
            return render(request, 'filesystem/filemanage.html', {'list': objects})


def stu_file(request):
    my_id = request.session['user_id']
    my_file = models.FileModel.objects.filter(file_owner=my_id)
    os.system('python D:\\project\\server\\filesystem\\doc2pdf.py')
    return render(request, 'filesystem/stu_file.html', {'list': my_file})



def readFile(filename, chunk_size=512):
    """文件读取函数"""
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







