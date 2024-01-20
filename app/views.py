from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

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
            return HttpResponse('registered successfully')
        else:
            return HttpResponse('Invalid Data')
    return render(request,'registration.html',d)