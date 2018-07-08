from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.contrib.auth.models import Permission

# Create your views here.

def index(request):
    user = request.user
    classrooms = None
    if not user.is_active:
        print("Chưa đăng nhập")
    else:
        if user.userprofile.headline == "Manager" or user.is_superuser:
            classrooms = Class.objects.all()
            print("Super")
        elif user.userprofile.headline == "Teacher":
            classrooms = user.userprofile.teacher.all()
            print("Teacher")
        elif user.userprofile.headline == "Supporter":
            classrooms = user.userprofile.supporter.all()
            print("Support")

    # classrooms = Class.objects.all()
    date_list = [d.time for d in Diary.objects.all()]
    date_list = sorted(date_list)
    context = {
        'classrooms': classrooms,
        'date_list': date_list
    }

    return render(request, "homepage.html", context = context)

def detail(request, pk):
    classroom = get_object_or_404(Class, pk = pk)
    if classroom != None:
        if request.user.userprofile.headline == "Supporter":
            notes = classroom.diary.filter(author = request.user).order_by('-time')
        else:
            notes = classroom.diary.all().order_by('-time')

    context = {
        'classroom': classroom,
        "notes" : notes,
    }
    return render(request, "detail.html", context = context)

support_permission = ['Can add diary', 'Can change diary', 'Can delete diary', 'Can add note precise', 'Can change note precise', 'Can delete note precise']

manager_permission = ['Can add diary', 'Can change diary', 'Can delete diary', 'Can add note precise', 'Can change note precise', 'Can delete note precise', 'Can add user', 'Can change user', 'Can delete user', 'Can add permission', 'Can change permission', 'Can delete permission', 'Can add class', 'Can change class', 'Can delete class', 'Can add user profile', 'Can change user profile', 'Can delete user profile']

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.userprofile.headline = form.cleaned_data.get("headline")
            user.is_staff = True
            user.save()
            
            headline = user.userprofile.headline
            if headline == "Supporter" or headline == "Teacher":
                for permiss in support_permission:
                    permission = Permission.objects.get(name=permiss)
                    user.user_permissions.add(permission)

            elif headline == "Manager":
                for permiss in manager_permission:
                    permission = Permission.objects.get(name=permiss)
                    user.user_permissions.add(permission)

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'uform': form})
