from django.shortcuts import render
from .models import Todo
from .form import TodoForm
from django.http import HttpResponseRedirect
from django.urls import reverse




# Create your views here.
def home(request):
    todos = Todo.objects.all()
    context = {"todos": todos}
    return render(request, 'todo/home.html', context)


def create_todo(request):
    form = TodoForm()
    context = {'form':form}

    if request.method == 'POST':
        title = request.POST.get('title')
        desciption = request.POST.get('description')
        is_completed = request.POST.get('is_completed', False)

        todo = Todo()    
        todo.title = title
        todo.description = desciption
        todo.is_completed = True if is_completed == 'on' else False
        todo.save()

        return HttpResponseRedirect(reverse('todo', kwargs={'id':todo.pk}))
        
    return render(request, 'todo/create_todo.html', context)

def todo_detail(request,id):
    context = {}
    return render(request,'todo/todo_detail.html', context)

