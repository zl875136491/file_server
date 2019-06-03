from django.shortcuts import render, redirect
# from .forms import NoteForm
from . import models
# Create your views here.


def noteediter(request):
    if request.method == "POST":
        title = request.POST.get('title', None)
        content = request.POST.get('content', None)
        deadline_date = request.POST.get('deadline_date', None)
        same_title = models.Notes.objects.filter(title=title)
        if same_title:
            message = '标题已经存在！'
            return render(request, 'notesystem/noteediter.html', locals())
        if not content:
            message = '无内容！'
            return render(request, 'notesystem/noteediter.html', locals())
        if not deadline_date:
            message = '无截止日期！'
            return render(request, 'notesystem/noteediter.html', locals())
        else:
            # 发布成功
            new_note = models.Notes.objects.create()
            new_note.title = title
            new_note.content = content
            new_note.deadline_date = deadline_date
            new_note.author = request.session['user_name']
            new_note.save()
            message = "发布成功!"
            return render(request, 'notesystem/publishok.html', locals())
    return render(request, 'notesystem/noteediter.html')


def notereciver(request):
    all_note = models.Notes.objects.all().order_by('publish_date')
    return render(request, 'notesystem/notereciver.html', {'list': all_note})


def notecontent(request, note_id):
    detail = models.Notes.objects.get(id=note_id)
    return render(request, 'notesystem/notecontent.html', {'list': detail})


def publishok(request):
    pass
    return render(request, 'notesystem/publishok.html')
