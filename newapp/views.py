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
from .forms import TaggingForm  
from .models import User, Tag, UserTag







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
    token = 'EAAb5iwsH0RUBPSENEf1CW3OgMo8bjfQRuG3PT1smRsNEYJWimKVjw0l9zfKLo8009E79YDi5xeNhPuTvNlwc2hZCPXHBKXjUI6ClVvQgFnQJEYPZBwBEJdJh3hr5Hg9W7xm2nMfcVrZBVr68g9Qx1C2Fpd4kUPuN5uER7jMleexmpy0w6B1m5bq4IlYEBMEAgZDZD'
    phone_id = '1356495696480176'
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

# import requests
# from datetime import datetime
# from django.shortcuts import render
# from django.views.decorators.csrf import csrf_exempt
# from newapp.models import User, Message
# from django.http import HttpResponse

# @csrf_exempt
# def send_whatsapp_message(request):
#     if request.method != 'POST':
#         # Only accept POST requests
#         return HttpResponse("Method not allowed", status=405)

#     phone_number_id = request.POST.get('phone_number_id', '')
#     phone = request.POST.get('phone', '')
#     message = request.POST.get('message', '')
#     response_data = None
#     success_message = None
#     error_message = None

#     if phone == '':
#         return HttpResponse("Phone number missing", status=400)

#     token = Admin.objects.filter(whatsapp_phone_id=phone_number_id).values_list('whatsapp_token', flat=True).first()
#     if token is None or token == '':
#         return HttpResponse("WhatsApp token missing", status=400)

#     url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
#     headers = {
#         "Authorization": f"Bearer {token}",
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "messaging_product": "whatsapp",
#         "to": phone,
#         "type": "text",
#         "text": {"body": message}
#     }

#     try:
#         res = requests.post(url, json=payload, headers=headers)
#         response_data = res.json()

#         if res.status_code == 200 and "messages" in response_data:
#             success_message = "✅ Message sent successfully!"
#             existing_user = User.objects.filter(phone_no=phone).first()
#             if not existing_user:
#                 new_user = User.objects.create(
#                     name='bot',
#                     phone_no=phone,
#                     created_at=datetime.now()
#                 )
#                 user_id = new_user.id
#             else:
#                 user_id = existing_user.id

#             if user_id is not None:
#                 user_instance = User.objects.get(id=user_id)
#                 Message.objects.create(
#                     user_id=user_instance,
#                     messages=message,
#                     created_at=datetime.now(),
#                     who='bot'
#                 )
#         else:
#             error_detail = response_data.get("error", {}).get("message", "Unknown error")
#             error_message = f"❌ Failed to send message: {error_detail}"

#     except Exception as e:
#         error_message = f"❌ Exception occurred: {str(e)}"

#     # Always return an HttpResponse or render at end
#     return render(request, 'send_message.html', {
#         'response': response_data,
#         'success_message': success_message,
#         'error_message': error_message
#     })




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


# @csrf_exempt
# def get_message(request):
#     verify_token = "speeed"  # must match what's in Meta dashboard

#     # ✅ Webhook verification (GET)
#     if request.method == 'GET':
#         mode = request.GET.get('hub.mode')
#         token = request.GET.get('hub.verify_token')
#         challenge = request.GET.get('hub.challenge')

#         if mode == 'subscribe' and token == verify_token:
#             return HttpResponse(challenge, status=200)
#         else:
#             return HttpResponse("Token verification failed", status=403)

#     # ✅ Webhook message (POST)
#     elif request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             # print("Webhook Data:", json.dumps(data, indent=2))

#             entry = data.get('entry', [])[0]
#             changes = entry.get('changes', [])[0]
#             value = changes.get('value', {})
#             messages = value.get('messages', [])[0]

#             phone = messages.get('from')  # WhatsApp number
#             msg_text = messages.get('text', {}).get('body')

#             existing_user = User.objects.filter(phone_no=phone).first()

#             if not existing_user:
#                 existing_user = User.objects.create(
#                     name='user',
#                     phone_no=phone,
#                     created_at=datetime.now()
#                 )
#                 print(f"✅ New user created: {existing_user.id}")

#             Message.objects.create(
#                 user_id=existing_user,
#                 messages=msg_text,
#                 created_at=datetime.now(),
#                 who='human'
#             )

#             pc = Pinecone(
#                 api_key='pcsk_2ayS93_Mo3c98NYEpDXKoSWadNcjjtwAmCPwDJ8Yj3jWHpMhtpvxA5aqSMawtxPYYmRgq1')

#             assistant = pc.assistant.Assistant(assistant_name="yahi")

#             msg = Pinemessage(content=msg_text)
#             resp = assistant.chat(messages=[msg])

#             bot_response = resp["message"]["content"]  # content
#             print(bot_response)
#             phone_number = phone
#             payload = {
#                 "phone": phone_number,
#                 "message": bot_response
#             }
#             response = requests.post(
#                 "https://494b6c088862.ngrok-free.app/send_whatsapp_message/", data=payload)
#             # exit
#             chunks = assistant.chat(messages=[msg], stream=True)


# # With streaming

#             return HttpResponse("Message stored", status=200)

#         except Exception as e:
#             print("Webhook Error:", str(e))
#             return HttpResponse(f"Error: {str(e)}", status=400)


def broadcast_msg(request):
    return render(request, 'broadcast_form.html')


WHATSAPP_API_URL = "https://graph.facebook.com/v22.0/1356495696480176/messages"
ACCESS_TOKEN = "EAAb5iwsH0RUBPSENEf1CW3OgMo8bjfQRuG3PT1smRsNEYJWimKVjw0l9zfKLo8009E79YDi5xeNhPuTvNlwc2hZCPXHBKXjUI6ClVvQgFnQJEYPZBwBEJdJh3hr5Hg9W7xm2nMfcVrZBVr68g9Qx1C2Fpd4kUPuN5uER7jMleexmpy0w6B1m5bq4IlYEBMEAgZDZD"  # your WhatsApp Cloud API token


# views.py
# views.py

WHATSAPP_API_URL ="https://graph.facebook.com/v22.0/1356495696480176/messages"
ACCESS_TOKEN ='EAAb5iwsH0RUBPSENEf1CW3OgMo8bjfQRuG3PT1smRsNEYJWimKVjw0l9zfKLo8009E79YDi5xeNhPuTvNlwc2hZCPXHBKXjUI6ClVvQgFnQJEYPZBwBEJdJh3hr5Hg9W7xm2nMfcVrZBVr68g9Qx1C2Fpd4kUPuN5uER7jMleexmpy0w6B1m5bq4IlYEBMEAgZDZD'


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

# def dashboard_view(request):
#     admin_id=request.session.get('admin_id')
#     # return HttpResponse(admin_id)
#     user=Admin.objects.filter(id=admin_id).only('display_phone_no').first()
#     display_phone_number=''.join((user.display_phone_no).split())
#     # return HttpResponse(display_phone_number)
#     # return HttpResponse(phone_id.whatsapp_phone_id)
#     user_phone=f"https://wa.me/{display_phone_number}"
#     # return HttpResponse(user_phone)
#     count=User.objects.count()
#     return render(request, 'dashboard.html',{'count':count,'phone_id':user_phone})
def dashboard_view(request):
    admin_id = request.session.get('admin_id')
    user = Admin.objects.filter(id=admin_id).only('display_phone_no', 'whatsapp_token', 'whatsapp_phone_id').first()
    
    display_phone_number = ''.join((user.display_phone_no).split()) if user else ''
    user_phone = f"https://wa.me/{display_phone_number}"

    whatsapp_connected = bool(user and user.whatsapp_token)

    count = User.objects.count()
    active_contacts_count = 0  # Replace with your logic if available

    context = {
        'count': count,
        'phone_id': user_phone,
        'whatsapp_connected': whatsapp_connected,
        'active_contacts_count': active_contacts_count,
    }
    return render(request, 'dashboard.html', context)


def inbox_view(request):
    return render(request, 'inbox.html')

def flows_view(request):
    return render(request, 'flows.html')

def contacts_view(request):
    return render(request, 'contacts.html')

def settings_view(request):
    return render(request, 'settings.html')




from django.shortcuts import render, redirect
from .forms import TaggingForm
from .models import Tag, User, UserTag
@csrf_exempt
def tag_view(request):
    if request.method == 'POST':
        form = TaggingForm(request.POST)
        if form.is_valid():
            tag_name = form.cleaned_data['tag_name']
            selected_users = form.cleaned_data['users']
            tag, created = Tag.objects.get_or_create(name=tag_name)

            # Delete all existing users from this tag
            UserTag.objects.filter(tag=tag).delete()

            # Add users from submitted form
            for user in selected_users:
                UserTag.objects.get_or_create(user=user, tag=tag)

            return redirect('add_tag')
        else:
            print("Form errors:", form.errors)
    else:
        # Display form for editing or creating
        form = TaggingForm()
        tag_name = request.GET.get('tag_name', None)
        if tag_name:
            tag = Tag.objects.filter(name=tag_name).first()
            if tag:
                users_of_tag = User.objects.filter(usertag__tag=tag)
                form = TaggingForm(initial={
                    'tag_name': tag.name,
                    'users': users_of_tag,
                })
    # supply tag_list as before
    tag_list = []
    tags = Tag.objects.all()
    for tag in tags:
        tagged_users = User.objects.filter(usertag__tag=tag)
        tag_list.append({'tag': tag, 'users': tagged_users})

    return render(request, 'contact/tag.html', {
        'form': form,
        'tag_list': tag_list,
    })


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import User

@login_required
def user_search_api(request):
    q = request.GET.get('q', '')
    users = User.objects.filter(name__icontains=q)[:20]
    results = [{'id': user.id, 'text': user.name} for user in users]
    return JsonResponse({'items': results})

# google_calendar

import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pytz

# ====== CONFIG ======
SERVICE_ACCOUNT_FILE = "credentials/service-account.json"  # Adjust path
CALENDAR_ID = "aravindkumarpro012@gmail.com"  # Replace with your Google Calendar ID
TIMEZONE = "Asia/Kolkata"
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def get_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build("calendar", "v3", credentials=creds)


def create_event(date_str, time_str="10:00", title="Appointment", description="", duration_minutes=60):
    service = get_service()
    tz = pytz.timezone(TIMEZONE)
    start_dt = tz.localize(datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M"))
    end_dt = start_dt + timedelta(minutes=duration_minutes)

    event_body = {
        "summary": title,
        "description": description,
        "start": {"dateTime": start_dt.isoformat(), "timeZone": TIMEZONE},
        "end": {"dateTime": end_dt.isoformat(), "timeZone": TIMEZONE},
    }

    event = service.events().insert(calendarId=CALENDAR_ID, body=event_body).execute()
    return event.get('htmlLink')


from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render
# from .google_calendar import create_event  # Import your create_event function from where you defined it


# @csrf_protect
# def create_event_api(request):
#     success_message = None
#     error_message = None

#     if request.method == "POST":
#         date = request.POST.get("date")
#         time = request.POST.get("time", "10:00")
#         title = request.POST.get("title", "Appointment")
#         description = request.POST.get("description", "")
#         duration = request.POST.get("duration", "60")

#         try:
#             duration = int(duration)
#         except ValueError:
#             duration = 60

#         try:
#             event_link = create_event(date, time, title, description, duration)
#             success_message = f"Event '{title}' created successfully! <a href='{event_link}' target='_blank'>View Event</a>"
#         except Exception as e:
#             error_message = f"Failed to create event: {str(e)}"

#     return render(request, 'calendar/form.html', {
#         'success_message': success_message,
#         'error_message': error_message,
#     })
@csrf_exempt
def create_event_api(request):
    success_message = None
    error_message = None

    if request.method == "POST":
        date = request.POST.get("date")
        time = request.POST.get("time", "10:00")
        title = request.POST.get("title", "Appointment")
        description = request.POST.get("description", "")
        duration = request.POST.get("duration", "60")
        user_email = request.POST.get("user_email", "Unknown user")  # <-- get user_email from form
        admin_id = request.POST.get("admin_id", "Unknown admin")
        user_id = request.POST.get("user_id", "Unknown user")

        try:
            duration = int(duration)
        except ValueError:
            duration = 60

        # Append user email to event description
        full_description = f"Created by: {user_email}\n\n{description}"

        try:
            event_link = create_event(date, time, title, full_description, duration)  # use full_description
            success_message = f"Event '{title}' created successfully! <a href='{event_link}' target='_blank'>View Event</a>"
        except Exception as e:
            error_message = f"Failed to create event: {str(e)}"

    return render(request, 'calendar/form.html', {
        'success_message': success_message,
        'error_message': error_message,
        'admin_id': admin_id,
        'user_id': user_id,
        'user_email': user_email,
    })

#chat gpt part
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required  # use if needed
from newapp.models import Admin  # or wherever you store the API keys
import openai

@csrf_exempt
def chatgpt_respond(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_prompt = data.get("prompt", "").strip()
            if not user_prompt:
                return JsonResponse({"error": "Prompt cannot be empty."}, status=400)

            admin = Admin.objects.first()
            if not admin or not admin.openai_api_key:
                return JsonResponse({"error": "ChatGPT API key not configured."}, status=403)

            openai.api_key = admin.openai_api_key

            response = openai.ChatCompletion.create(
                model="gpt-4",  # or "gpt-3.5-turbo"
                messages=[{"role": "user", "content": user_prompt}],
            )
            reply = response.choices[0].message.content

            # Here you can also add your logic to send this reply back to WhatsApp user if needed

            return JsonResponse({"reply": reply})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)

from django.shortcuts import render, redirect
from .models import ChatGPTPrompt
@csrf_exempt
def chatgpt_prompt_page(request):
    prompt_obj = ChatGPTPrompt.objects.first()
    current_prompt = prompt_obj.prompt_text if prompt_obj else ""

    if request.method == "POST":
        new_prompt = request.POST.get("prompt_text", "").strip()
        if prompt_obj:
            prompt_obj.prompt_text = new_prompt
            prompt_obj.save()
        else:
            ChatGPTPrompt.objects.create(prompt_text=new_prompt)
        return redirect('chatgpt_prompt_page')

    return render(request, 'chatgpt_prompt.html', {"prompt": current_prompt})

@csrf_exempt
def get_message_chatgpt(request):
    if request.method != "POST":
        return HttpResponse(status=200)

    try:
        data = json.loads(request.body)
        entry = data.get('entry', [])[0]
        changes = entry.get('changes', [])[0]
        value = changes.get('value', {})
        messages_list = value.get('messages', [])

        if not messages_list:
            return HttpResponse("No messages", status=400)

        messages = messages_list[0]
        phone = messages.get('from')  # WhatsApp number
        user_text = messages.get('text', {}).get('body')

        admin = Admin.objects.first()
        if not admin or not admin.openai_api_key:
            return HttpResponse("ChatGPT API key not configured", status=400)

        # Save incoming message
        user_obj, _ = User.objects.get_or_create(
            phone_no=phone,
            defaults={'name': 'user', 'created_at': datetime.now()}
        )
        Message.objects.create(
            user_id=user_obj,
            messages=user_text,
            created_at=datetime.now(),
            who='human'
        )

        prompt_obj = ChatGPTPrompt.objects.first()
        common_prompt = prompt_obj.prompt_text if prompt_obj else ""

        chatgpt_input = f"{common_prompt}\n\nUser: {user_text}" if common_prompt else user_text

        # Call OpenAI API
        openai.api_key = admin.openai_api_key
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": chatgpt_input}],
        )
        reply = response.choices[0].message.content

        # Save reply
        Message.objects.create(
            user_id=user_obj,
            messages=reply,
            created_at=datetime.now(),
            who='bot'
        )

        # Send reply back via WhatsApp
        whatsapp_api_url = f"https://graph.facebook.com/v17.0/{admin.whatsapp_phone_id}/messages"
        headers = {
            "Authorization": f"Bearer {admin.whatsapp_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": phone,
            "type": "text",
            "text": {"body": reply}
        }
        requests.post(whatsapp_api_url, json=payload, headers=headers)

        return HttpResponse("ChatGPT message processed", status=200)

    except Exception as e:
        print(f"ChatGPT webhook error: {str(e)}")
        return HttpResponse(f"Error: {str(e)}", status=400)

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Admin


@csrf_exempt
def connect_openai_key(request):
    if request.method == "POST":
        data = json.loads(request.body.decode("utf-8"))
        api_key = data.get("api_key", "").strip()
        if not api_key:
            return JsonResponse({"msg": "API key is required."}, status=400)

        admin = Admin.objects.first()
        if not admin:
            return JsonResponse({"msg": "Admin not found."}, status=404)

        # Disconnect Pinecone
        admin.pinecone_token = ""

        # Save ChatGPT API key
        admin.openai_api_key = api_key
        admin.save(update_fields=['pinecone_token', 'openai_api_key'])
        return JsonResponse({"msg": "ChatGPT API key connected. Pinecone disconnected."})
    return JsonResponse({"msg": "Invalid request."}, status=405)

@csrf_exempt
def disconnect_openai_key(request):
    if request.method == "POST":
        admin = Admin.objects.first()
        if not admin:
            return JsonResponse({"msg": "Admin not found."}, status=404)

        admin.openai_api_key = ""
        admin.save(update_fields=['openai_api_key'])
        return JsonResponse({"msg": "ChatGPT API key disconnected."})
    return JsonResponse({"msg": "Invalid request."}, status=405)
