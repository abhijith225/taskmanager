from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from datetime import datetime
from django.urls import reverse
from .models import *

def home(request):
    return render(request, "Basic/index.html", {})

def register(request):
    success = False 
    print("hello")   
    if request.method == "POST":
        print("world")   
        username = request.POST["username"]
        password = request.POST["password"]
        Users.objects.create(username=username,
                             password=password)
        success = True
    return render(request, "Admin/Register.html", {"success": success})

def switch_user(request):
    users = Users.objects.all()
    if request.method == "POST":
        username = request.POST["user"]
        user = Users.objects.get(username=username)
        request.session["username"] = user.username
        request.session["role"] = user.role
        return redirect("home")
    return render(request, "Basic/SwitchUser.html", {"users": users})

def add_task(request):
    users = Users.objects.filter(role="User")
    success = error = False
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        assigned_to = Users.objects.filter(username=request.POST["assigned_to"])
        priority = request.POST["priority"]
        try:
            instance = Task(title=title,
                            description=description,
                            created_by=Users.objects.get(username=request.session["username"]),
                            assigned_to=assigned_to[0] if assigned_to else None,
                            priority=priority)
            instance.full_clean()
            instance.save()
            success = True
        except IntegrityError:
            error = "This title is already added"
        except ValidationError:
            error = "Priority must be between 1 and 5"
    return render(request, "user/AddTask.html", {"users": users,
                                                 "success": success,
                                                 "error": error})

def view_tasks(request):
    tasks = Task.objects.all()
    return render(request, "Basic/ViewTasks.html", {"tasks": tasks})

def update_task(request, id):
    users = Users.objects.filter(role="User")
    success = error = False
    task = Task.objects.get(id=id)
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        assigned_to = Users.objects.filter(username=request.POST["assigned_to"])
        priority = int(request.POST["priority"])
        if priority < 1 or priority > 5:
            error = "Priority must be between 1 and 5"
        else:
            try:
                Task.objects.filter(id=id).update(title=title,
                                                description=description,
                                                assigned_to=assigned_to[0] if assigned_to else None,
                                                priority=priority, 
                                                updated_at=datetime.now())
                success = True
            except IntegrityError:
                error = "This title is already added"
    return render(request, "user/AddTask.html", {"users": users,
                                                 "task": task,
                                                 "success": success,
                                                 "error": error})

def update_status(request, id, old_status):
    transitions = {
            "Pending": ["In Progress"],
            "In Progress": ["Done", "Cancelled"],
            "Done": [], 
            "Cancelled": [] 
        }
    error = False
    if request.method == "POST":
        new_status = request.POST["new_status"]
        if new_status in transitions[old_status]:
            Task.objects.filter(id=id).update(status=new_status)
            instance = TaskHistory(task=Task.objects.get(id=id),
                                   changed_by=Users.objects.get(username=request.session["username"]),
                                   change_details=f"Status changed from {old_status} to {new_status}")
            instance.save()
            return redirect(reverse('update_status', kwargs={'id': id, 'old_status': new_status}))
        else:
            error = "Invalid Status Transition"
    return render(request, "Basic/UpdateStatus.html", {"transitions": transitions.keys(),
                                                       "error": error})

def delete_task(request, id):
    TaskHistory.objects.create(task=Task.objects.get(id=id),
                               changed_by=Users.objects.get(username=request.session["username"]),
                               change_details=f"Task Id. {id} has been deleted")
    Task.objects.filter(id=id).delete()
    return redirect("view_tasks")

def task_history(request, id):
    task = Task.objects.get(id=id)
    history =  TaskHistory.objects.filter(task=task)
    return render(request, "Basic/TaskHistory.html", {"history": history})