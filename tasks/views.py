from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {"tasks": tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {"tasks": tasks})

@login_required
def create_task(request):
    if request.method == "GET":
        return render(request, 'create_task.html', {"form": TaskForm()})
    else:
        try:
            form = TaskForm(request.POST, request.FILES)
            if form.is_valid():
                new_task = form.save(commit=False)
                new_task.user = request.user
                new_task.save()
                return redirect('tasks')
            else:
                return render(request, 'create_task.html', {
                    "form": form, 
                    "error": "Error al crear la tarea. Verifica los datos."
                })
        except ValueError:
            return render(request, 'create_task.html', {
                "form": TaskForm(request.POST, request.FILES), 
                "error": "Error al crear la tarea."
            })

def home(request):
    return render(request, 'home.html')

@login_required
def signout(request):
    logout(request)
    return render(request, 'home.html')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Username or password is incorrect."})

        login(request, user)
        return redirect('tasks') 

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, request.FILES, instance=task)
            if form.is_valid():
                form.save()
                return redirect('tasks')
            else:
                return render(request, 'task_detail.html', {
                    'task': task, 
                    'form': form, 
                    'error': 'Error al actualizar la tarea. Verifica los datos.'
                })
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task, 
                'form': TaskForm(request.POST, request.FILES, instance=task), 
                'error': 'Error al actualizar la tarea.'
            })
        

@login_required
def edit_tasks(request, task_id):
    print(f"DEBUG: edit_tasks llamada con task_id={task_id}")
    print(f"DEBUG: Método: {request.method}")
    
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        print(f"DEBUG: Tarea encontrada: {task.title}")
        form = TaskForm(instance=task)
        print(f"DEBUG: Formulario creado: {form}")
        print("DEBUG: Renderizando template edit_task.html")
        return render(request, 'edit_task.html', {'task': task, 'form': form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, request.FILES, instance=task)
            if form.is_valid():
                form.save()
                print("DEBUG: Tarea guardada exitosamente")
                return redirect('tasks')
            else:
                print(f"DEBUG: Errores del formulario: {form.errors}")
                return render(request, 'edit_task.html', {
                    'task': task, 
                    'form': form, 
                    'error': 'Error al actualizar la tarea. Verifica los datos.'
                })
        except ValueError as e:
            print(f"DEBUG: ValueError: {e}")
            return render(request, 'edit_tasks.html', {
                'task': task, 
                'form': TaskForm(request.POST, request.FILES, instance=task), 
                'error': 'Error al actualizar la tarea.'
            })



@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    task.datecompleted = timezone.now()
    task.save()
    return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    task.delete()
    return redirect('tasks')
    
@login_required
def total_tasks(request):
    user_tasks = Task.objects.filter(user=request.user)

    context = {
        'total_tasks': user_tasks.count(),
        'total_pending': user_tasks.filter(datecompleted__isnull=True, important=False).count(),
        'total_inprogress': user_tasks.filter(datecompleted__isnull=True, important=True).count(),
        'total_completed': user_tasks.filter(datecompleted__isnull=False).count(),
        'tasks': user_tasks.order_by('-created')
    }

    return render(request, 'dashboard.html', context)

        
