from django.shortcuts import render, redirect

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm      # on utilisera des chose toutes faites de django  
from django.contrib.auth import authenticate, login, logout
from django.contrib  import messages  # on aura besoin de ça aussi 

# Create your views here.

def login_user(request):
    if request.method == 'POST':
        print ("is posted")
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        
        if user is not None:
            login(request, user)
            return redirect("omtv:dashboard")
        else:            
            messages.info(request, "Identifiant ou mot de passe incorrect")    

    # si pas POST
    form = AuthenticationForm()
    return render(request, "accounts/login.html", {"form" : form})

def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("omtv:programmes")        
    else:
        form = UserCreationForm()    
    return render(request, "accounts/register.html", {"form" : form})
        
def logout_user(request):
    logout(request)
    return redirect("omtv:programmes")
