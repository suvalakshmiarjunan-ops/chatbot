from django.http import HttpResponse
from django.shortcuts import render,redirect
from ..models import User
from ..models import Message
from django.contrib import messages
from newapp.models import Admin
from datetime import datetime

class Contactcontroller:

    def dashboard(request):
        # get admin_id from session
        admin_id = request.session.get("admin_id")

        if not admin_id:
            return redirect("/login")   # or return an error if not logged in

        # filter users by admin_id
        users = User.objects.filter(admin_id=admin_id)

        return render(request, "contact/dashboard.html", {"users": users})
    
    def add_user(request):
        return render(request,'contact/add_user.html')
    
    def add_admin_user(request):
        # return HttpResponse('hi')
        if(request.method=='POST'):
            name=(request.POST.get('name').strip() or '').strip()
            phone_no=(request.POST.get('phone_no')or '').strip()
            if name=='' or phone_no=='':
                messages.warning(request,'name and phone fields cannot be empty')
            if(not User.objects.filter(phone_no=phone_no)):
                admin_id=Admin.objects.get(id=request.session.get('admin_id'))
                User.objects.create(
                    admin_id=admin_id,
                    name=name,
                    phone_no=phone_no,
                    created_at=datetime.now()
                )
                messages.success(request,'successfully inserted')
                return redirect(request.META.get("HTTP_REFERER", "contact/add"))
            else:
                 messages.warning(request,'already mobile number exists')
                 return redirect(request.META.get("HTTP_REFERER", "contact/add"))
        else:
            return HttpResponse('not correct method')
        
        