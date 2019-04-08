from django.shortcuts import render, redirect
from .forms import NoteForm
from . import models
# Create your views here.


# def noteediter(request):
#     pass
#     return render(request, 'notesystem/noteediter.html')


def notereciver(request):
    pass
    return render(request, 'notesystem/notereciver.html')


def noteediter(request):

    if request.method == "POST":
        title = request.POST.get('title', None)
        content = request.POST.get('content', None)
        deadline_date = request.POST.get('deadline_date', None)
        print(title, content, deadline_date)
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
            new_note = models.Notes.objects.create()
            new_note.title = title
            new_note.content = content
            new_note.deadline_date = deadline_date
            new_note.author = request.session['user_name']
            new_note.save()
            message = "Successful!"
            return render(request, 'notesystem/notereciver.html', locals())
    return render(request, 'notesystem/noteediter.html')

