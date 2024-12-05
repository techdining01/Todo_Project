from django.shortcuts import render, get_object_or_404, redirect
from .models import Todo
from .form import TodoForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required






def get_todos(request, todos):
    if request.GET and request.GET.get('filter'):
        if request.GET.get('filter') == 'completed':
            return todos.filter(is_completed=True)
        if request.GET.get('filter') == 'incomplete':
            return todos.filter(is_completed=False)

    return todos


@login_required
def home(request):
    todos = Todo.objects.all()
    completed = todos.filter(is_completed=True).count()
    incompleted = todos.filter(is_completed=False).count()
    total = todos.count()
    context = {"todos": get_todos(request, todos), 'completed': completed, 'incompleted': incompleted, 'total':total}
    print(incompleted)
    return render(request, 'todo/home.html', context)



@login_required
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
        todo.owner = request.user
        todo.save()
        messages.add_message(request, messages.SUCCESS, 'Todo created successfully')
        return HttpResponseRedirect(reverse('home'))
        
    return render(request, 'todo/create_todo.html', context)


@login_required
def todo_detail(request,id):
    todo = get_object_or_404(Todo, pk=id)
    context = {'todo': todo}
    if todo.owner != request.user:
        messages.add_message(request, messages.ERROR, "You cannot Edit todo that doesn't belong to you")
        return HttpResponseRedirect(reverse('home'))

    return render(request,'todo/todo_detail.html', context)
    


@login_required
def delete_todo(request, id):
    todo = get_object_or_404(Todo, pk=id)
    context = {"todo":todo}
    if request.method == 'POST':
        if todo.owner != request.user:
            
            messages.add_message(request, messages.ERROR, "You cannot delete todo that doesn't belong to you")
            return HttpResponseRedirect(reverse('home'))
        
        todo.delete()
        messages.add_message(request, messages.SUCCESS, 'Todo deleted successfully')
        return HttpResponseRedirect(reverse('home'))

    return render(request,'todo/delete_todo.html', context)



@login_required
def update_todo(request, id):
    todo = get_object_or_404(Todo, pk=id)
    form = TodoForm(instance=todo)
    context = {"todo": todo, "form":form}
    title = request.POST.get('title')
    description = request.POST.get('description')
    is_completed = request.POST.get(is_completed, False)

    if todo.owner != request.user :
        messages.add_message(request, messages.ERROR, "You cannot Edit todo that doesn't belong to you")
        return redirect(reverse('home'))

    if request.method == "POST":
        
        todo.title = title
        todo.description = description
        todo.is_completed = True if is_completed == 'on' else False
        todo.save()
        messages.add_message(request, messages.SUCCESS, 'Todo updated successfully')
        return redirect(reverse('home'))
    
    return render(request,'todo/update_todo.html', context)