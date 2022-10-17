from asyncio.base_subprocess import BaseSubprocessTransport
import email
# from pyexpat.errors import messages
from django.contrib import messages
from re import sub
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth.decorators import login_required

# Create your views here.


def home(request):
    return render(request, 'home.html')


@login_required(login_url='/login')
def cursos(request):
    
    return render(request, 'home.html')


@login_required(login_url='/login')
def progresso(request):
    
    return render(request, 'home.html')


@login_required(login_url='/login')
def perfil(request):
    
    return render(request, 'home.html')


def sobre(request):
    
    return render(request, 'home.html')


def cadastro(request):
    if request.method == 'GET':
        return render (request, 'cadastro.html')
    else:
        nome = request.POST.get('nome')
        sobrenome = request.POST.get('sobrenome')
        email = request.POST.get('email')
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        count_nums = 0
        # checagem de caracteres
        for c in nome:
            if c.isdigit():
                count_nums += 1
        if count_nums > 0:
            messages.info(request, 'O nome deve conter apenas letras')
            return redirect('cadastro')
        if len(nome.strip()) == 0 or len(email.strip()) == 0 or len(username.strip()) == 0:
            messages.info(request, 'Favor inserir corretamente nos campos nome, email e usuário.')
            return redirect('cadastro')
        if len(senha) < 6 or len(senha) > 10:
            messages.info(request, 'Favor inserir senha com no mínimo 6 e no máximo 10 caracteres')
            return redirect('cadastro')
    # contadores
    count_alpha = 0
    count_nums = 0
    # checagem de caracteres
    for c in senha:
        if c.isalpha():
            count_alpha += 1
        elif c.isdigit():
            count_nums += 1
    if count_alpha == 0 or count_nums == 0:
        messages.info(request, 'A senha deve conter letras e números')
        return redirect('cadastro')
    user = User.objects.filter(email=email).first()
    if user:
        messages.info(request, 'Esse email de usuário já está cadastrado em nosso sistemas!')
        return redirect('cadastro')
    else:
        user = User.objects.filter(username=username).first()
        if user:
            messages.info(request, 'Já existe um usuário com esse username!')
            return redirect('cadastro') 
        else:
            user = User.objects.create_user(first_name = nome, last_name = sobrenome, email = email, username = username, password = senha)
            user.save()
            messages.info(request, 'Usuário cadastrado com sucesso!')
            return redirect('home')



def login(request):
    if request.method == 'GET':
        return render (request, 'login.html')
    else:
        username = request.POST.get('usuario')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)
        if user:
            login_django(request, user)
            return render(request, 'home.html')
        else:
            messages.info(request, 'Usuário ou senha inválidos!')
            return redirect('login')
        

def logout(request):
    logout_django(request)
    return render(request, 'home.html')
    

