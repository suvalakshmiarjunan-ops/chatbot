from django.http import HttpResponse
from django.http import JsonResponse
import requests
from ..models import Admin
from django.shortcuts import redirect
from django.contrib import messages
from newapp.models import User
from django.shortcuts import redirect, render
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message as Pinemessage
from newapp.models import Message
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime


class whatsappcontroller:
    @csrf_exempt
    def connect(request):
        phone_id = request.POST.get('phone_id') or ''
        user_token = request.POST.get('user_token') or ''

        headers = {
            'Authorization': f"Bearer {user_token}"
        }
        url = f"https://graph.facebook.com/v21.0/{phone_id}"

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status() 

            if (response.status_code == 200):
                response_data = response.json()
                display_phone_no = str(
                    response_data.get('display_phone_number', ''))
                admin_id = request.session.get('admin_id')
                if admin_id:
                    Admin.objects.filter(id=admin_id).update(
                        whatsapp_phone_id=phone_id,
                        whatsapp_token=user_token,
                        display_phone_no=display_phone_no
                    )
                    messages.success(request, "whatsapp connected")
                    return redirect(request.META.get('HTTP_REFERER', '/'))
                messages.success(request, "whatsapp not connected")
                return redirect(request.META.get('HTTP_REFERER', '/'))
            # print(response_data)
        except requests.exceptions.RequestException as e:
            messages.warning(request, "whatsapp error try again later")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        messages.warning(request, "server error")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    @csrf_exempt
    def send_whatsapp_message(request):
        end=True
        if end is True:
            phone_number_id=request.POST.get('phone_number_id')
            
            
            response_data = None
            success_message = None
            error_message = None
            phone = request.POST.get('phone') or ''
            if (phone == ''):
                return
            
            token = Admin.objects.filter(whatsapp_phone_id=phone_number_id).values_list('whatsapp_token', flat=True).first()
          

            if request.method == 'POST':
                # phone = request.POST.get('phone')
                message = request.POST.get('message')
                print(message)

                url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
                headers = {
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "messaging_product": "whatsapp",
                    "to": phone,
                    "type": "text",
                    "text": {
                        "body": message
                    }
                }
                try:
                    res = requests.post(url, json=payload, headers=headers)
                    response_data = res.json()
                    end=False

                    if res.status_code == 200 and "messages" in response_data:
                        success_message = "✅ Message sent successfully!"
                        existing_user = User.objects.filter(phone_no=phone).first()
                        if not existing_user:
                            new_user = User.objects.create(
                                name='bot',
                                phone_no=phone,
                                created_at=datetime.now()
                            )
                            user_id = new_user.id
                            print(f"id:{user_id}")
                        else:
                            user_id = existing_user.id
                            print(f"User already exist ID:{user_id}")
                        if user_id is not None:
                            user_instance = User.objects.get(id=user_id)
                            new_message = Message.objects.create(
                                user_id=user_instance,
                                messages=message,
                                created_at=datetime.now(),
                                who='bot'
                            )
                            print(f"successfully")
                        else:
                            print('sorry')
                    else:
                        error_detail = response_data.get(
                            "error", {}).get("message", "Unknown error")
                        error_message = f"❌ Failed to send message: {error_detail}"

                except Exception as e:
                    error_message = f"❌ Exception occurred: {str(e)}"
        return

    @csrf_exempt
    def get_message(request):
        end = True
        VERIFY_TOKEN = "speeed"
        if end is True:
            if request.method == 'GET':
                mode = request.GET.get('hub.mode')
                token = request.GET.get('hub.verify_token')
                challenge = request.GET.get('hub.challenge')

                if mode == 'subscribe' and token == VERIFY_TOKEN:
                    return HttpResponse(challenge, status=200)
                else:
                    return HttpResponse("Token verification failed", status=403)

            elif request.method == 'POST':
                try:
                    data = json.loads(request.body)

                    entry = data.get('entry', [])[0]
                    changes = entry.get('changes', [])[0]
                    value = changes.get('value', {})
                    messages = value.get('messages', [])[0]
                    meta_data = value.get("metadata", {})
                    phone_number_id = meta_data.get('phone_number_id')
                    # print(phone_number_id)
                    admin_check = Admin.objects.filter(
                        whatsapp_phone_id=phone_number_id).first()
                    print(admin_check.pinecone_token)
                    if not admin_check:
                        return
                    phone = messages.get('from')  # WhatsApp number
                    msg_text = messages.get('text', {}).get('body')

                    existing_user = User.objects.filter(phone_no=phone).first()

                    if not existing_user:
                        admin_id = request.session.get('admin_id')
                        admin_oid = Admin.objects.get(id=admin_id)
                        existing_user = User.objects.create(
                            name='user',
                            admin_id=admin_oid,
                            phone_no=phone,
                            created_at=datetime.now()
                        )
                        print(f"✅ New user created: {existing_user.id}")

                    Message.objects.create(
                        user_id=existing_user,
                        messages=msg_text,
                        created_at=datetime.now(),
                        who='human'
                    )

                    pc = Pinecone(
                        api_key=admin_check.pinecone_token)

                    assistant = pc.assistant.Assistant(assistant_name="yahi")

                    msg = Pinemessage(content=msg_text)
                    resp = assistant.chat(messages=[msg])

                    bot_response = resp["message"]["content"]  # content
                    print(bot_response)
                    phone_number = phone
                    payload = {
                        "phone": phone_number,
                        "message": bot_response,
                        "phone_number_id": phone_number_id
                    }
                    response = requests.post(
                        "https://07377353818c.ngrok-free.app/send_whatsapp_message/", data=payload)
                    
                    end = False
                    return HttpResponse("Message stored", status=200)

                except Exception as e:
                    print("Webhook Error:", str(e))
                    return HttpResponse(f"Error: {str(e)}", status=400)
