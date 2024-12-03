from django.shortcuts import render

# Create your views here.

def register(request):

    if request.method == "POST":
        pass

    return render(request, 'authentication/register.html')


def login(request):
    return render(request, 'authentication/login.html')

