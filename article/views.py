from django.shortcuts import render
from user import  until
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Anthology,Article
import time
from django.utils import timezone

# Create your views here.
@csrf_exempt
def writer(request):
    userProfile = request.user
    edit_article = None
    if request.method == 'GET' and userProfile.is_active:
        anths = Anthology.objects.filter(user=userProfile).order_by('date')
        if not anths:
            articles = []
            anths = []
            anthology = Anthology.objects.create(name='日记本',user=userProfile)
            anths.append(anthology)
            title = time.strftime('%Y-%m-%d', time.localtime())
            article = Article.objects.create(anthology=anthology, title=title)
            articles.append(article)
            edit_article = article
        else:
            edit_article = Article.objects.filter(anthology__user=userProfile).order_by('-last_edit')[0]
            articles = Article.objects.filter(anthology=edit_article.anthology).order_by('date')
        return render(request,'article/writer.html',{'anths':anths,'articles':articles,'edit_article':edit_article})

@csrf_exempt
def up_load(request):
    ret_json ={
        "errno": -1,
        # "msg": "图片上传失败" ,
    }

    userProfile = request.user
    if request.method == 'POST' and userProfile.is_active:
        file = request.FILES.get('file')
        # print(request.POST)
        edit_article = Article.objects.filter(anthology__user=userProfile).order_by('-last_edit')[0]
        icon_url = 'User/' + userProfile.username + '/aticle/images/' + str(edit_article.id)
        icon_url = until.save_image(file,icon_url,file.name)
        ret_json['errno'] = 0
        # ret_json['msg'] = '图片上传成功'
        ret_json['data'] =  [
             '/media/'+icon_url
        ]
    return HttpResponse(json.dumps(ret_json), content_type="application/json")

@csrf_exempt
def update_anth_name(request):
    ret = {'status':0}
    if request.method == 'POST' and request.user.is_active:
        name = request.POST.get('name')
        anth = Article.objects.filter(anthology__user=request.user).order_by('-last_edit')[0].anthology
        anth.name = name
        anth.save()
        ret['status'] = 1
    return HttpResponse(json.dumps(ret), content_type="application/json")

@csrf_exempt
def del_anth(request):
    ret = {'status':0}
    if request.method == 'POST' and request.user.is_active:
        anth = Article.objects.filter(anthology__user=request.user).order_by('-last_edit')[0].anthology
        anth.delete()
        ret['status'] = 1
    return HttpResponse(json.dumps(ret), content_type="application/json")

@csrf_exempt
def create_anth(request):
    if request.method == 'POST' and request.user.is_active:
        name = request.POST.get('name')
        if name == '':
            return render(request, 'error.html')
        userProfile = request.user
        anth = Anthology.objects.create(name=name,user=userProfile)
        title = time.strftime('%Y-%m-%d', time.localtime())
        Article.objects.create(anthology=anth, title=title)
        return HttpResponseRedirect('/article/writer')
    return render(request,'error.html')

@csrf_exempt
def create_article(request):
    ret = {'status': 0}
    if request.method == 'POST' and request.user.is_active:
        anth = Article.objects.filter(anthology__user=request.user).order_by('-last_edit')[0].anthology
        title = time.strftime('%Y-%m-%d', time.localtime())
        Article.objects.create(anthology=anth, title=title)
        ret['status'] = 1
    return HttpResponse(json.dumps(ret), content_type="application/json")

@csrf_exempt
def change_anth(request):
    ret = {'status': 0}
    if request.method == 'POST' and request.user.is_active:
        anth = Anthology.objects.get(id=request.POST.get('id'))
        articles = Article.objects.filter(anthology=anth).order_by('-last_edit')
        if articles:
            articles[0].last_edit=timezone.now()
            articles[0].save()
        else:
            title = time.strftime('%Y-%m-%d', time.localtime())
            Article.objects.create(title=title,anthology=anth)
        ret['status'] = 1
    return HttpResponse(json.dumps(ret), content_type="application/json")

@csrf_exempt
def change_article(request):
    ret = {'status': 0}
    if request.method == 'POST' and request.user.is_active:
        article = Article.objects.get(id=request.POST.get('id'))
        article.last_edit=timezone.now()
        article.save()

        ret['status'] = 1
    return HttpResponse(json.dumps(ret), content_type="application/json")

@csrf_exempt
def set_article_title(request):
    ret = {'status': 0}
    if request.method == 'POST' and request.user.is_active:
        article = Article.objects.get(id=request.POST.get('id'))
        article.title = request.POST.get('title')
        article.save()

        ret['status'] = 1
    return HttpResponse(json.dumps(ret), content_type="application/json")

@csrf_exempt
def save_article(request):
    ret = {'status': 0}
    if request.method == 'POST' and request.user.is_active:
        article = Article.objects.get(id=request.POST.get('id'))
        article.content = request.POST.get('content')
        article.save()

        ret['status'] = 1
    return HttpResponse(json.dumps(ret), content_type="application/json")


@csrf_exempt
def change_public(request):
    ret = {'status': 0}
    if request.method == 'POST' and request.user.is_active:
        article = Article.objects.get(id=request.POST.get('id'))
        is_public = article.is_public
        article.is_public = not is_public
        article.save()

        ret['status'] = 1
    return HttpResponse(json.dumps(ret), content_type="application/json")
@csrf_exempt
def del_article(request):
    ret = {'status': 0}
    if request.method == 'POST' and request.user.is_active:
        article = Article.objects.get(id=request.POST.get('id'))
        anth = article.anthology
        article.delete()
        if not Article.objects.filter(anthology=anth):
            title = time.strftime('%Y-%m-%d', time.localtime())
            Article.objects.create(title=title, anthology=anth)
        ret['status'] = 1
    return HttpResponse(json.dumps(ret), content_type="application/json")

@csrf_exempt
def move_article(request):
    ret = {'status': 0}
    if request.method == 'POST' and request.user.is_active:
        article = Article.objects.get(id=request.POST.get('article_id'))
        anth_new = Anthology.objects.get(id=request.POST.get('anth_id'))
        anth_old = article.anthology
        article.anthology = anth_new
        article.save()
        if not Article.objects.filter(anthology=anth_old):
            title = time.strftime('%Y-%m-%d', time.localtime())
            Article.objects.create(title=title, anthology=anth_old)
        ret['status'] = 1
    return HttpResponse(json.dumps(ret), content_type="application/json")

def read_article(request,article_id):
    article = Article.objects.filter(id=article_id)
    if article and  (article[0].is_public or article[0].anthology.user == request.user):
        return render(request, 'article/article.html', {'article': article[0]})

    return  render(request,'error.html')
