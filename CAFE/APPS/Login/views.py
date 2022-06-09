from django.shortcuts import redirect, render
from APPS.Login.models import User

def login(request):
    context = {
        'error': '',
    }
    if request.method == 'GET':
        return render(request, 'login.html', context)
    elif request.method == 'POST':
        uid = request.POST.get('uid', None)
        pw = request.POST.get('password', None)

        if not uid and not pw:
            context['error'] = "아이디와 비밀번호를 모두 입력하세요."
        else:
            try:
                user = User.objects.get(user_id=uid)
            except User.DoesNotExist:
                user = None

            if not user:
                context['error'] = '없는 계정입니다.'
            elif not pw == user.pw:
                context['error'] = '비밀번호가 틀립니다.'
            else:
                context['User'] = user.user_id
                request.session['User'] = user.user_id
                return render(request, 'loginok.html', context)
        return render(request, 'login.html', context)

def logout(request):
    if request.session.get('User'):
        del(request.session['User'])

    context = {
        'error': '',
    }

    return render(request, 'logout.html', context)

def join(request):
    context = {
        'User': request.session.get('User'),
    }

    if request.method =='GET':
        return render(request, 'join.html', context)
    elif request.method == 'POST':
        uid = request.POST['uid']
        pw = request.POST['pw']

        try:
            user = User.objects.get(user_id=uid)
        except User.DoesNotExist:
            user = None

        if user:
            context['error'] = '이미 존재하는 아이디입니다.';
            return render(request, 'join.html', context)
        else:
            userT = User(
                uid = uid,
                pw= pw)
            userT.save() 
        return render(request, 'login.html')

def needlogin(request):
    return render(request, "needlogin.html")

def loginok(request):

    return render(request, 'loginok.html')

def needlogin2(request):
    return render(request, 'needlogin2.html')