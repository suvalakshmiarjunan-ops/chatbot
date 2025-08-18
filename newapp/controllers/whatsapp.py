from django.http import HttpResponse
from django.http import JsonResponse
import requests
from ..models import Admin
from django.shortcuts import redirect
from django.contrib import messages

class whatsappcontroller:
    
     def connect(request):
        # response_data =[]
        phone_id = request.POST.get('phone_id') or ''
        user_token = request.POST.get('user_token') or ''

        headers = {
            'Authorization': f"Bearer {user_token}"
        }
        url = f"https://graph.facebook.com/v21.0/{phone_id}"

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises error for bad responses
            # print(type(response_data))
            # print(response_data['verified_name'])
        
            if(response.status_code==200):
                response_data = response.json()
                display_phone_no=str(response_data.get('display_phone_number',''))
                # return HttpResponse(str(response_data.get('display_phone_number','')))
                admin_id=request.session.get('admin_id')
                if admin_id:
                    Admin.objects.filter(id=admin_id).update(
                        whatsapp_phone_id=phone_id,
                        whatsapp_token=user_token,
                        display_phone_no=display_phone_no
                    )
                    messages.success(request,"whatsapp connected")
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                messages.success(request,"whatsapp not connected")
                return redirect(request.META.get('HTTP_REFERER', '/'))
            # print(response_data)
        except requests.exceptions.RequestException as e:
                messages.warning(request,"whatsapp error try again later")
                return redirect(request.META.get('HTTP_REFERER', '/'))

        messages.warning(request,"server error")
        return redirect(request.META.get('HTTP_REFERER', '/'))