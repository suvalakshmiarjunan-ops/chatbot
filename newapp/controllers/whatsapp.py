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
from urllib.parse import urlencode
from django.utils import timezone
import openai
from newapp.models import ChatGPTPrompt



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
           
        except requests.exceptions.RequestException as e:
            messages.warning(request, "whatsapp error try again later")
            return redirect(request.META.get('HTTP_REFERER', '/'))

        messages.warning(request, "server error")
        return redirect(request.META.get('HTTP_REFERER', '/'))

    @csrf_exempt
    def send_whatsapp_message(request):
        if request.method != 'POST':
            return JsonResponse({"error": "Method not allowed"}, status=405)

        phone_number_id = (request.POST.get('phone_number_id') or '').strip()
        phone = (request.POST.get('phone') or '').strip()
        message = (request.POST.get('message') or '').strip()

        if not phone:
            return JsonResponse({"error": "Phone number missing"}, status=400)

        token = Admin.objects.filter(whatsapp_phone_id=phone_number_id)\
                            .values_list('whatsapp_token', flat=True).first()
        if not token:
            return JsonResponse({"error": "WhatsApp token missing"}, status=400)

        url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        payload = {
            "messaging_product": "whatsapp",
            "to": phone,
            "type": "text",
            "text": {"body": message}
        }

        try:
            res = requests.post(url, json=payload, headers=headers, timeout=20)
            try:
                data = res.json()
            except Exception:
                data = {"raw_text": res.text}

            if res.status_code == 200 and "messages" in data:
                # persist bot message (uses timezone.now)
                user = User.objects.filter(phone_no=phone).first()
                if not user:
                    user = User.objects.create(name='bot', phone_no=phone, created_at=timezone.now())
                Message.objects.create(user_id=user, messages=message, created_at=timezone.now(), who='bot')
                return JsonResponse({"ok": True, "provider_response": data}, status=200)
            else:
                err = (data.get("error") or {}).get("message") or data
                return JsonResponse({"ok": False, "provider_response": err}, status=502)

        except Exception as e:
            return JsonResponse({"ok": False, "exception": str(e)}, status=500)

    
    # @csrf_exempt
    # def send_whatsapp_message(request):
    #     if request.method == 'GET':
    #         # Render the send message form on GET requests
    #         return render(request, 'send_message.html')

    #     elif request.method == 'POST':
    #         phone_number_id = request.POST.get('phone_number_id', '')
    #         phone = request.POST.get('phone', '')
    #         message = request.POST.get('message', '')

    #         if phone == '':
    #             return HttpResponse("Phone number missing", status=400)

    #         token = Admin.objects.filter(whatsapp_phone_id=phone_number_id).values_list('whatsapp_token', flat=True).first()
    #         if token is None or token == '':
    #             return HttpResponse("WhatsApp token missing", status=400)

    #         response_data = None
    #         success_message = None
    #         error_message = None

    #         url = f"https://graph.facebook.com/v17.0/{phone_number_id}/messages"
    #         headers = {
    #             "Authorization": f"Bearer {token}",
    #             "Content-Type": "application/json"
    #         }
    #         payload = {
    #             "messaging_product": "whatsapp",
    #             "to": phone,
    #             "type": "text",
    #             "text": {"body": message}
    #         }

    #         try:
    #             res = requests.post(url, json=payload, headers=headers)
    #             response_data = res.json()

    #             if res.status_code == 200 and "messages" in response_data:
    #                 success_message = "✅ Message sent successfully!"
    #                 existing_user = User.objects.filter(phone_no=phone).first()
    #                 if not existing_user:
    #                     new_user = User.objects.create(
    #                         name='bot',
    #                         phone_no=phone,
    #                         created_at=datetime.now()
    #                     )
    #                     user_id = new_user.id
    #                 else:
    #                     user_id = existing_user.id

    #                 user_instance = User.objects.get(id=user_id)
    #                 Message.objects.create(
    #                     user_id=user_instance,
    #                     messages=message,
    #                     created_at=datetime.now(),
    #                     who='bot'
    #                 )
    #             else:
    #                 error_detail = response_data.get("error", {}).get("message", "Unknown error")
    #                 error_message = f"❌ Failed to send message: {error_detail}"

    #         except Exception as e:
    #             error_message = f"❌ Exception occurred: {str(e)}"

    #         return render(request, 'send_message.html', {
    #             'response': response_data,
    #             'success_message': success_message,
    #             'error_message': error_message,
    #             'phone_number_id': phone_number_id,
    #             'phone': phone,
    #             'message': message
    #         })

    #     else:
    #         return HttpResponse("Method not allowed", status=405)

    @csrf_exempt
    def get_message(request):
        VERIFY_TOKEN = "speeed"

        # Webhook verification
        if request.method == 'GET':
            mode = request.GET.get('hub.mode')
            token = request.GET.get('hub.verify_token')
            challenge = request.GET.get('hub.challenge')
            if mode == 'subscribe' and token == VERIFY_TOKEN:
                return HttpResponse(challenge, status=200)
            return HttpResponse("Token verification failed", status=403)

        # Webhook delivery
        if request.method == 'POST':
            try:
                data = json.loads(request.body.decode("utf-8"))

                entries = data.get('entry') or []
                if not entries:
                    return HttpResponse("OK", status=200)  # ack silently

                for entry in entries:
                    changes = entry.get('changes') or []
                    for change in changes:
                        value = change.get('value') or {}
                        metadata = value.get("metadata") or {}
                        phone_number_id = metadata.get('phone_number_id')

                        # Make sure we have an Admin for this number
                        admin_check = Admin.objects.filter(whatsapp_phone_id=phone_number_id).first()
                        if not admin_check:
                            continue  # ack but skip

                        # messages/statuses may be absent
                        for m in value.get('messages') or []:
                            if m.get('type') != 'text':
                                continue

                            phone = m.get('from')
                            msg_text = (m.get('text') or {}).get('body') or ""
                            if not msg_text.strip():
                                continue

                            # upsert user
                            existing_user = User.objects.filter(phone_no=phone).first()
                            if not existing_user:
                                existing_user = User.objects.create(
                                    name='user',
                                    admin_id=Admin.objects.get(id=admin_check.id),
                                    phone_no=phone,
                                    created_at=datetime.now(),
                                )

                            # save human message
                            try:
                                Message.objects.create(
                                    user_id=existing_user,
                                    messages=msg_text,
                                    created_at=datetime.now(),
                                    who='human'
                                )
                            except Exception as db_in_e:
                                print(f"DB inbound error: {db_in_e}")

                            # Trigger link?
                            bot_response = None
                            trigger = False
                            try:
                                if getattr(admin_check, "goolgle_calendar", "") != "":
                                    if any(word in msg_text.lower() for word in ['book', 'appointment']):
                                        payload = {"msg_text": msg_text.lower(), 'admin_id': admin_check.id, 'user_id': existing_user.id}
                                        send_request = requests.post(
                                            "https://2b526918e9a1.ngrok-free.app/send_trigger/",
                                            data=payload,
                                            timeout=10
                                        )
                                        send_request.raise_for_status()
                                        resp = send_request.json()
                                        bot_response = resp.get("url")
                                        trigger = True
                            except requests.RequestException as e:
                                # non-fatal; we’ll fallback to NL response
                                print(f"trigger error: {e}")

                            # If not trigger: Pinecone -> ChatGPT fallback
                            if not trigger:
                                # 1) Try Pinecone only if token exists
                                try:
                                    pine_token = getattr(admin_check, "pinecone_token", "") or ""
                                    if pine_token:
                                        pc = Pinecone(api_key=pine_token)
                                        assistant = pc.assistant.Assistant(assistant_name="yahi")
                                        pmsg = Pinemessage(content=msg_text)
                                        resp = assistant.chat(messages=[pmsg])
                                        bot_response = (resp or {}).get("message", {}).get("content")
                                except Exception as pe:
                                    print(f"Pinecone error: {pe}")

                                # 2) Fallback to ChatGPT if bot_response missing
                                # ---------------- LLM reply (ChatGPT first) ----------------
                                if not trigger:
                                    bot_response = None

                                    openai_key = (getattr(admin_check, "openai_api_key", "") or "").strip()
                                    pine_token = (getattr(admin_check, "pinecone_token", "") or "").strip()

                                    if openai_key:
                                        # ChatGPT path – uses your /chatgpt_prompt/ text as SYSTEM
                                        try:
                                            openai.api_key = openai_key

                                            prompt_obj = ChatGPTPrompt.objects.first()
                                            system_prompt = (prompt_obj.prompt_text or "").strip() if prompt_obj else ""
                                            if not system_prompt:
                                                system_prompt = (
                                                    "Follow the owner's configured instructions exactly. "
                                                    "If no instructions are configured, reply: 'Prompt not configured.'"
                                                )

                                            resp = openai.ChatCompletion.create(
                                                # openai==0.28.1 interface
                                                model="gpt-3.5-turbo",  # or "gpt-4" if your key has access
                                                messages=[
                                                    {"role": "system", "content": system_prompt},
                                                    {"role": "user", "content": msg_text},
                                                ],
                                                timeout=15,
                                            )
                                            bot_response = resp.choices[0].message.content.strip()
                                            print("[LLM] ChatGPT used")
                                        except Exception as oe:
                                            print(f"[LLM] OpenAI error: {oe}")
                                            bot_response = "Sorry, I couldn’t generate a response just now."

                                    elif pine_token:
                                        # Pinecone path – ONLY if ChatGPT isn’t configured
                                        try:
                                            pc = Pinecone(api_key=pine_token)
                                            assistant = pc.assistant.Assistant(assistant_name="yahi")
                                            pmsg = Pinemessage(content=msg_text)
                                            presp = assistant.chat(messages=[pmsg])
                                            bot_response = (presp or {}).get("message", {}).get("content")
                                            print("[LLM] Pinecone used")
                                        except Exception as pe:
                                            print(f"[LLM] Pinecone error: {pe}")
                                            bot_response = "Sorry, I couldn’t generate a response just now."
                                    else:
                                        bot_response = "Sorry, my assistant is offline right now."

                                    if not bot_response:
                                        bot_response = "Got it!"
                                # ---------------- /LLM reply ----------------

                            # Send back via your sender endpoint
                            payload = {
                                "phone": phone,
                                "message": bot_response,
                                "phone_number_id": phone_number_id
                            }
                            try:
                                r = requests.post(
                                    "https://2b526918e9a1.ngrok-free.app/send_whatsapp_message/",
                                    data=payload,
                                    timeout=15
                                )
                                if r.status_code != 200:
                                    print(f"WA send error {r.status_code}: {r.text}")
                            except Exception as se:
                                print(f"WA send exception: {se}")

                            # Save bot reply
                            try:
                                Message.objects.create(
                                    user_id=existing_user,
                                    messages=bot_response,
                                    created_at=datetime.now(),
                                    who='bot'
                                )
                            except Exception as db_out_e:
                                print(f"DB bot save error: {db_out_e}")

                return HttpResponse("Message stored", status=200)

            except Exception as e:
                print(f"Webhook Error: {str(e)}")
                # return 200 so WA doesn't retry aggressively
                return HttpResponse("OK", status=200)

        # not GET/POST
        return HttpResponse("Method not allowed", status=405)
    @csrf_exempt
    def send_trigger(request):
        admin_id=request.POST.get('admin_id') or ''
        user_id=request.POST.get('user_id') or ''
        if user_id=='' or admin_id =='':
            return JsonResponse({'status':False})
        origin = request.build_absolute_uri('/')[:-1]
        # qs=urlencode({'admin_id':admin_id,'user_id':user_id})
        return JsonResponse({
            'status':True,
            'url':f"{origin}/appointment_date/?admin_id={admin_id}&&user_id={user_id}&&calendar_id=aravindkumarpro012@gmail.com"
        })
        # return None
    def appointment_date(request):
        return render(request,'calendar/form.html')
    
    def disconnect(request):
        
        admin_id=request.session.get('admin_id')
        Admin.objects.filter(id=admin_id).update(whatsapp_phone_id='', whatsapp_token='')
        messages.warning(request, 'Invalid email or password')
        return redirect('/setting/channels')
        

