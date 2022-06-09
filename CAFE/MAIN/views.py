from django.shortcuts import render


def main(request):
    context = {
        'user' : request.session.get("User")
    }
    
    return render(request, 'main.html', context)