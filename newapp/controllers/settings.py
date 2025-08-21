from django.http import HttpResponse
from django.shortcuts import render,redirect
from ..models import Admin

class Settingcontroller :
    def dashboard(request):
        # return HttpResponse('hi')
        return render(request,'set/dashboard.html')
    def channels_view(request):
        # return render(re)
        whatsapp_connected=None
        admin_id=request.session.get('admin_id')
        if admin_id:
            admin=Admin.objects.filter(id=admin_id).only('whatsapp_phone_id','whatsapp_token').first()
            if admin:
              if admin.whatsapp_token!='' and admin.whatsapp_phone_id!='':
                  whatsapp_connected=True
        # return HttpResponse(whatsapp_connected)
        # return HttpResponse(whatsapp_connected)
        return render(request,'set/channels.html',{'whatsapp_connected':whatsapp_connected})