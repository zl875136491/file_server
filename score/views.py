from django.shortcuts import render
from notesystem import models as note_models
from filesystem import models as file_models
from . import models


def checkscore(request):
    author = request.session['user_name']
    title = request.session['title_todo']
    if request.method == "POST":
        owner_list = request.POST.getlist('owner', '')
        score_list = request.POST.getlist('score', '')
        for i, j in zip(owner_list, score_list):
            fingerprint = str(title) + str(i)
            if not models.Score.objects.filter(score_fp=fingerprint):
                item = models.Score.objects.create()
                item.score_owner = i
                item.score = j
                item.score_checker = author
                item.score_attribution = title
                item.score_fp = fingerprint
                item.save()
            else:
                message = '该学生分数已提交，请勿重复提交！'
                return render(request, 'score/checkscorenotok.html', locals())
        return render(request, 'score/checkscoreok.html')
    else:
        return render(request, 'score/checkscore.html')


def selecltile(request):
    author = request.session['user_name']
    own_note = note_models.Notes.objects.filter(author=author)
    if request.method == "POST":
        title_todo = request.POST.get('title_todo')
        request.session['title_todo'] = title_todo
        submited_stu = file_models.FileModel.objects.filter(file_attribution=title_todo)
        return render(request, 'score/checkscore.html', {'list': submited_stu})
    else:
        return render(request, 'score/selecttitle.html', {'list': own_note})


def checkscoreok(request):
    pass
    return render(request, 'score/checkscoreok.html', locals())


def checkscorenotok(request):
    pass
    return render(request, 'score/checkscorenotok.html', locals())


def seescore(request):
    scorer = request.session['user_id']
    all_score = models.Score.objects.filter(score_owner=scorer)
    return render(request, 'score/seescore.html', {'list': all_score})



