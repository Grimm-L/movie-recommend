from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from Top250.CBRecommend import CBRecommend
from Top250.models import Top250, Tags, UserRatedmovies, Users


def Login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == "POST":
        usm = request.POST.get('usm')
        pwd = request.POST.get('pwd')
        if Users.objects.filter(username=usm):
            if Users.objects.filter(username=usm)[0].password == pwd:
                # return HttpResponse('登录成功')
                return HttpResponseRedirect('http://127.0.0.1:8000/index/')
            else:
                return HttpResponse('密码错误')
        else:
            HttpResponse('用户不存在')
    return render(request, 'login.html')

def Register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        # password = make_password(password)
        Users.objects.create(username=name, password=password)
        return HttpResponseRedirect('/login/')

def movies(request):
    movies = Top250.objects.all();
    tagsTotal = Tags.objects.all();
    paginator = Paginator(movies,10);
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    is_paginated = True if paginator.num_pages > 1 else False
    context = {'page_obj':page_obj, 'is_paginated':is_paginated, 'tagsTotal':tagsTotal}
    return render(request,'index.html',context)

@csrf_protect
def detail(request,id):
    detail = Top250.objects.filter(id=id);
    rating = request.POST.get('rate')
    user = UserRatedmovies.objects.filter(Q(rating=rating) & Q(movieid=id))
    userid = 0
    movieid = 0
    rec = {}
    for i in user:
        userid = i.userid
        movieid = i.movieid
        cb = CBRecommend(K=5)
        movies_m = cb.recommend(userid)
        rec = Top250.objects.filter(id__in=movies_m)
    content = {'detail':detail, 'user':user,'userid':userid,'movieid':movieid,'rec':rec}
    return render(request,'detail.html', content)

def type(request, id):
    tagname = Tags.objects.get(id=id);
    tn = tagname.value
    movies_tags = Top250.objects.filter(type__contains=tn);
    paginator = Paginator(movies_tags, 10);
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    is_paginated = True if paginator.num_pages > 1 else False
    content = {'movies_tags':movies_tags, 'tagname':tagname,'tn':tn, 'page_obj':page_obj, 'is_paginated':is_paginated}
    return render(request, 'type.html', content)

