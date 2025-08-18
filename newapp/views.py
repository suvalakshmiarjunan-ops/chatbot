from .models import User, Message
from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import User
from datetime import datetime
# from .models import Message
from pinecone_plugins.assistant.models.chat import Message as Pinemessage

from django.http import JsonResponse
from pinecone import Pinecone

from django.utils import timezone
from .models import Message
from .models import Admin


def voice_bot(request):
    return render(request, 'voice_bot.html')


@csrf_exempt
def connect_whatsapp(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        phone_id = request.POST.get('phone_id')
        request.session['token'] = token
        request.session['phone_id'] = phone_id
        return redirect('send_whatsapp_message')  # go to chat screen
    return render(request, 'connect_whatsapp.html')


@csrf_exempt
def send_whatsapp_message(request):
    response_data = None
    success_message = None
    error_message = None

    # token = request.session.get('token')
    token = 'EAAJDRQ3tmhcBPGZCMDOPZAgNSBZBRjT42NP56LwPZBTAdUJcQfyQJMqjdaxWiWGQBPdC8rDzrp4SFzvFy8nn2wJHkWtb73imDcoZBvtKmoilvZAydQS0zFdnSoFpiRmVNwzAhwjtdYFE6kiBXdp9zZAZA3VZAmjGREnQXflNSK4eFqfF6sMp5oZBdH3U4GZAmACK3L5kgZDZD'
    phone_id = '659162020619134'
    # token = 'EAAJDRQ3tmhcBPGZCMDOPZAgNSBZBRjT42NP56LwPZBTAdUJcQfyQJMqjdaxWiWGQBPdC8rDzrp4SFzvFy8nn2wJHkWtb73imDcoZBvtKmoilvZAydQS0zFdnSoFpiRmVNwzAhwjtdYFE6kiBXdp9zZAZA3VZAmjGREnQXflNSK4eFqfF6sMp5oZBdH3U4GZAmACK3L5kgZDZD'
    # phone_id = request.session.get('phone_id')

    if request.method == 'POST':
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(message)

        url = f"https://graph.facebook.com/v17.0/{phone_id}/messages"
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

    return render(request, 'send_message.html', {
        'response': response_data,
        'success_message': success_message,
        'error_message': error_message
    })


@csrf_exempt
def send_voice_bot(request):
    response_data = None
    success_message = None
    error_message = None

    if request.method == 'POST':
        phone = request.POST.get('phone')
        task_message = request.POST.get('message')

        url = "https://us.api.bland.ai/v1/calls"
        headers = {
            "Authorization": "org_75c71ec310d8a684abda84f7449f8d677907dff8520f3be866b24a349d36525a11c4999655477378608569",
            "Content-Type": "application/json"
        }
        payload = {
            "phone_number": phone,
            "task": task_message
        }

        try:
            res = requests.post(url, json=payload, headers=headers)
            response_data = res.json()

            # ✅ Check for success response based on actual API format
            if res.status_code == 200 and response_data.get("status") == "success":
                call_id = response_data.get("call_id", "N/A")
                success_message = f"✅ Voice call queued successfully! Call ID: {call_id}"
            else:
                error_detail = response_data.get("message", "Unknown error")
                error_message = f"❌ Failed to initiate call: {error_detail}"

        except Exception as e:
            error_message = f"❌ Exception occurred: {str(e)}"

    return render(request, 'voice_bot.html', {
        'response': response_data,
        'success_message': success_message,
        'error_message': error_message
    })


def show_people(request):
    users = User.objects.all().values('id', 'phone_no')
    return render(request, 'show_people.html', {'users': users})


# views.py
def show_chatbox(request):
    users = User.objects.only('id', 'phone_no').order_by('id')
    selected_user_id = request.GET.get('user_id')

    selected_user = None
    messages = []

    if selected_user_id:
        selected_user = User.objects.filter(id=selected_user_id).first()
        messages = Message.objects.filter(user_id=selected_user_id).order_by('created_at')

    return render(request, 'show_people.html', {
        'users': users,
        'selected_user': selected_user,
        'messages': messages,
    })


# @csrf_exempt
# def send_whatsapp_message(request):
#     response_data = None
#     token = request.session.get('token')
#     phone_id = request.session.get('phone_id')

#     if request.method == 'POST':
#         phone = request.POST.get('phone')
#         message = request.POST.get('message')

#         url = f"https://graph.facebook.com/v17.0/{phone_id}/messages"
#         headers = {
#             "Authorization": f"Bearer {token}",
#             "Content-Type": "application/json"
#         }
#         payload = {
#             "messaging_product": "whatsapp",
#             "to": phone,
#             "type": "text",
#             "text": {
#                 "body": message
#             }
#         }

#         res = requests.post(url, json=payload, headers=headers)
#         response_data = res.json()

#     return render(request, 'send_message.html', {'response': response_data})


@csrf_exempt
def get_message(request):
    verify_token = "speeed"  # must match what's in Meta dashboard

    # ✅ Webhook verification (GET)
    if request.method == 'GET':
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')

        if mode == 'subscribe' and token == verify_token:
            return HttpResponse(challenge, status=200)
        else:
            return HttpResponse("Token verification failed", status=403)

    # ✅ Webhook message (POST)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            # print("Webhook Data:", json.dumps(data, indent=2))

            entry = data.get('entry', [])[0]
            changes = entry.get('changes', [])[0]
            value = changes.get('value', {})
            messages = value.get('messages', [])[0]

            phone = messages.get('from')  # WhatsApp number
            msg_text = messages.get('text', {}).get('body')

            existing_user = User.objects.filter(phone_no=phone).first()

            if not existing_user:
                existing_user = User.objects.create(
                    name='user',
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

            # # replace with dynamic number

            # payload = {
            #     "phone": phone_number,
            #     "message": bot_response
            #     }
            # # response msg send
            # print(msg_text)
            # print(phone)
            # return HttpResponse("Message stored", status=200)

            pc = Pinecone(
                api_key='pcsk_2ayS93_Mo3c98NYEpDXKoSWadNcjjtwAmCPwDJ8Yj3jWHpMhtpvxA5aqSMawtxPYYmRgq1')

            assistant = pc.assistant.Assistant(assistant_name="yahi")

            msg = Pinemessage(content=msg_text)
            resp = assistant.chat(messages=[msg])

            bot_response = resp["message"]["content"]  # content
            print(bot_response)
            phone_number = phone
            payload = {
                "phone": phone_number,
                "message": bot_response
            }
            response = requests.post(
                "https://46f76b389ec3.ngrok-free.app/send_whatsapp_message/", data=payload)
            # exit
            chunks = assistant.chat(messages=[msg], stream=True)


# With streaming

            return HttpResponse("Message stored", status=200)

        except Exception as e:
            print("Webhook Error:", str(e))
            return HttpResponse(f"Error: {str(e)}", status=400)


def broadcast_msg(request):
    return render(request, 'broadcast_form.html')


WHATSAPP_API_URL = "https://graph.facebook.com/v22.0/659162020619134/messages"
ACCESS_TOKEN = "EAAJDRQ3tmhcBPGZCMDOPZAgNSBZBRjT42NP56LwPZBTAdUJcQfyQJMqjdaxWiWGQBPdC8rDzrp4SFzvFy8nn2wJHkWtb73imDcoZBvtKmoilvZAydQS0zFdnSoFpiRmVNwzAhwjtdYFE6kiBXdp9zZAZA3VZAmjGREnQXflNSK4eFqfF6sMp5oZBdH3U4GZAmACK3L5kgZDZD"  # your WhatsApp Cloud API token


# views.py
# views.py

WHATSAPP_API_URL ="https://graph.facebook.com/v22.0/659162020619134/messages"
ACCESS_TOKEN ='EAAJDRQ3tmhcBPGZCMDOPZAgNSBZBRjT42NP56LwPZBTAdUJcQfyQJMqjdaxWiWGQBPdC8rDzrp4SFzvFy8nn2wJHkWtb73imDcoZBvtKmoilvZAydQS0zFdnSoFpiRmVNwzAhwjtdYFE6kiBXdp9zZAZA3VZAmjGREnQXflNSK4eFqfF6sMp5oZBdH3U4GZAmACK3L5kgZDZD'


def send_broadcast(request):
    if request.method != "POST":
        return HttpResponse("Invalid request method", status=405)

    msg = (request.POST.get('message') or '').strip()
    if not msg:
        return HttpResponse("Message is required", status=400)

    # Get all phones you intend to send to
    phones = list(User.objects.values_list('phone_no', flat=True))
    users = User.objects.filter(phone_no__in=phones).values('id', 'phone_no')
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    for user in users:
        user_instance = User.objects.get(id=user['id'])
        payload = {
        "messaging_product": "whatsapp",
        "to":user['phone_no'],
        "type": "template",
        "template": {
        "name": "hello_world",
        "language": {"code": "en_US"}
        }}
        r = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
        Message.objects.create(
            user_id=user_instance,
            messages="hello world",
            who="bot"
        )
    return HttpResponse(200)
         
   
   
    
    # print(phones)






    return HttpResponse(200,'yahi')

    
    users = User.objects.filter(phone_no__in=phones).values('id', 'phone_no')
    # phone_to_id = {str(u['phone_no']): u['id'] for u in users}

    # headers = {
    #     "Authorization": f"Bearer {ACCESS_TOKEN}",
    #     "Content-Type": "application/json"
    # }

    # results = []
    # messages_to_create = []

    # with transaction.atomic():
    #     for phone in phones:
    #         phone_str = str(phone)

    #         # Send WhatsApp template (hello_world)

    #         }

    #         r = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
    #         results.append(f"{phone_str}: {r.status_code} {r.text}")

    #         # Find user_id by phone and queue a Message row
    #         user_id = phone_to_id.get(phone_str)
    #         if user_id:
    #             messages_to_create.append(
    #                 Message(
    #                     user_id=user_id,
    #                     messages=msg,          # change to your actual field name if different
    #                     who='bot',             # adjust choices if needed
    #                     created_at=timezone.now(),  # if your model doesn't auto-add
    #                 )
    #             )

    #     # Insert messages in bulk (faster)
    #     if messages_to_create:
    #         Message.objects.bulk_create(messages_to_create, batch_size=500)

    # return HttpResponse("<br>".join(results))
from django.shortcuts import render

def dashboard_view(request):
    admin_id=request.session.get('admin_id')
    # return HttpResponse(admin_id)
    user=Admin.objects.filter(id=admin_id).only('display_phone_no').first()
    display_phone_number=''.join((user.display_phone_no).split())
    # return HttpResponse(display_phone_number)
    # return HttpResponse(phone_id.whatsapp_phone_id)
    user_phone=f"https://wa.me/{display_phone_number}"
    # return HttpResponse(user_phone)
    count=User.objects.count()
    return render(request, 'dashboard.html',{'count':count,'phone_id':user_phone})

def inbox_view(request):
    return render(request, 'inbox.html')

def flows_view(request):
    return render(request, 'flows.html')

def contacts_view(request):
    return render(request, 'contacts.html')

def settings_view(request):
    return render(request, 'settings.html')
