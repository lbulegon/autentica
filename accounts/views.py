from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from motopro.forms import LoginForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redireciona se já estiver logado

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Página após login bem-sucedido
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redireciona após logout
