from django.shortcuts import render

def chatmain(request):

    request.session.get('User')

    

    return render(request, 'chat_main.html')
