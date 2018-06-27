from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
# Create your views here.

def index(request):
    classrooms = Class.objects.all()
    date_list = [d.time for d in Diary.objects.all()]
    print(date_list)
    context = {
        'classrooms': classrooms,
        'date_list': date_list
    }

    return render(request, "homepage.html", context = context)

def detail(request, pk):
    classroom = get_object_or_404(Class, pk = pk)
    if classroom != None:
        notes = classroom.diary.all()

    context = {
        'classroom': classroom,
        "notes" : notes,
    }
    return render(request, "detail.html", context = context)


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.user_profile.headline = form.cleaned_data.get("headline")
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'uform': form})
