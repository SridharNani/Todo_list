from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate , login as loginUser , logout
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
# Create your views here.
from app.forms import TODOForm
from app.models import TODO
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

@login_required(login_url='login')
def home(request):
    if request.user.is_authenticated:
        user = request.user
        form = TODOForm()
        todos = TODO.objects.filter(user = user).order_by('priority')
        return render(request , 'index.html' , context={'form' : form , 'todos' : todos})

def login(request):
    if request.method == 'GET':
        form1 = AuthenticationForm()
        return render(request , 'login.html' ,{"form":form1} )
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username , password = password)
            if user is not None:
                loginUser(request , user)
                return redirect('home')
        else:
            return render(request , 'login.html' ,{"form":form} )


# def signup(request):
#     return render(request,'signup.html',{'form':UserCreationForm()})
#
# def save_user(request):
#     ucf = UserCreationForm(request.POST)
#     if ucf.is_valid():
#         ucf.save()
#         return redirect('main')
#     else:
#         return render(request, "signup.html", {"ucf": ucf})
def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request , 'signup.html' ,{'form':form})
    else:
        print(request.POST)
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            if user is not None:
                return redirect('login')
        else:
            return render(request , 'signup.html' ,{"form":form})



@login_required(login_url='login')
def add_todo(request):
    if request.user.is_authenticated:
        user = request.user
        print(user)
        form = TODOForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            todo = form.save(commit=False)
            todo.user = user
            todo.save()
            print(todo)
            return redirect("home")
        else:
            return render(request , 'index.html' , context={'form' : form})

#
def edit_todo(request, pk):

    # subject = 'welcome to GFG world'
    # message = f'Hi {user.username}, thank you for registering in folks.'
    # email_from = settings.EMAIL_HOST_USER
    # recipient_list = [user.email, ]
    # send_mail(subject, message, email_from, recipient_list)

    task = TODO.objects.get(id=pk)

    form = TODOForm(instance=task)

    if request.method == 'POST':
        form = TODOForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'edit.html', context)


def delete_todo(request , id ):
    print(id)
    # email=EmailMessage(
    #     'Confirm to Edit',
    #     'body',
    #     settings.EMAIL_HOST_USER,
    #     ['vickysridhar007@gmail.com']
    # )
    # email.fail_silently=False
    # email.send()
    TODO.objects.get(pk = id).delete()
    return redirect('home')

def change_todo(request , id  , status):
    todo = TODO.objects.get(pk = id)
    todo.status = status
    todo.save()
    return redirect('home')


def signout(request):
    logout(request)
    return redirect('login')