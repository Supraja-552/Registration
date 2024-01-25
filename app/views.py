from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
# Create your views here.
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from app.forms import * 
def registration(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}
    
    if request.method=='POST' and request.FILES:
        ufdo=UserForm(request.POST)
        pfdo=ProfileForm(request.POST,request.FILES)
        if ufdo.is_valid() and pfdo.is_valid():
            MUFDO=ufdo.save(commit=False)
            pw=ufdo.cleaned_data['password']
            MUFDO.set_password(pw)
            MUFDO.save()
            MPFDO=pfdo.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()
            send_mail('registration',
                      'Tanks for registered successfully',
                      'suprajachimmani2002@gmail.com',
                      [MUFDO.email],
                      fail_silently=True)
            return HttpResponse('registered successfully')
        else:
            return HttpResponse('Invalid Data')
    return render(request,'registration.html',d)
def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')
def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('Invalid credentials')
        
    return render(request,'user_login.html')
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
def profile_display(request):
    un=request.session['username']
    UO=User.objects.get(username=un)
    PO=Profile.objects.get(username=UO)
    d={'uo':UO,'po':PO}
    return render(request,'profile_display.html',d)