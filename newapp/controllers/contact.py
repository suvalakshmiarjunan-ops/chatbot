from django.http import HttpResponse
from django.shortcuts import render,redirect
from ..models import User
from ..models import Message

class Contactcontroller:
    def dashboard(request):
        users=User.objects.all()
      
        return render(request,'contact/dashboard.html',{'users':users})
        