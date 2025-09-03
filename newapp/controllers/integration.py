from django.http import JsonResponse
from django.http import HttpResponse
from newapp.models import Admin
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST


class Integrationcontroller:

    @csrf_exempt
    def connect(request):
        try:
            data = json.loads(request.body.decode("utf-8"))
            token = data.get("api_key") or ""
            if not token:
                return JsonResponse({"msg": "API key required"}, status=400)

            # Disconnect ChatGPT
            Admin.objects.update(openai_api_key='')

            # Connect Pinecone token
            Admin.objects.update(pinecone_token=token)

            return JsonResponse({
                "msg": "Pinecone connected; ChatGPT disconnected.",
                "token": token
            })
        except Exception as e:
            return JsonResponse({"msg": str(e)}, status=500)
    def disconnect(request):
        try:
            Admin.objects.update(pinecone_token='')
            return JsonResponse({'msg': 'Pinecone disconnected successfully.'})
        except Exception as e:
            return JsonResponse({'msg': str(e)}, status=500)    

# old one 
# class Integrationcontroller:
#     def dissconnect(request):
#        Admin.objects.update(pinecone_token='')
#        return JsonResponse({
#            'msg':'disconnected pinecone'
#        })
#     # @require_POST
#     @csrf_exempt
#     def connect(request):
#             try:
#                 data = json.loads(request.body.decode("utf-8"))
#                 token = data.get("api_key") or ""
#                 if not token:
#                     return JsonResponse({"msg": "API key required"}, status=400)
#                 Admin.objects.update(pinecone_token=token)
#                 return JsonResponse({
#                     "msg": "connected",
#                     "token": token
#                 })
#             except Exception as e:
#                 return JsonResponse({"msg": str(e)}, status=500)



# new one

# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from newapp.models import Admin

# class Integrationcontroller:

#     @csrf_exempt
#     def disconnect_pinecone(request):
#         Admin.objects.update(pinecone_token='')
#         return JsonResponse({'msg': 'Pinecone disconnected'})

#     @csrf_exempt
#     def disconnect_chatgpt(request):
#         Admin.objects.update(openai_api_key='')
#         return JsonResponse({'msg': 'ChatGPT disconnected'})

#     @csrf_exempt
#     def connect_pinecone(request):
#         try:
#             data = json.loads(request.body.decode("utf-8"))
#             token = data.get("api_key") or ""
#             if not token:
#                 return JsonResponse({"msg": "Pinecone API key required"}, status=400)

#             # Disconnect ChatGPT first
#             Admin.objects.update(openai_api_key='')

#             # Connect Pinecone token
#             Admin.objects.update(pinecone_token=token)
#             return JsonResponse({"msg": "Pinecone connected", "token": token})
#         except Exception as e:
#             return JsonResponse({"msg": str(e)}, status=500)

#     @csrf_exempt
#     def connect_chatgpt(request):
#         try:
#             data = json.loads(request.body.decode("utf-8"))
#             api_key = data.get("api_key") or ""
#             if not api_key:
#                 return JsonResponse({"msg": "ChatGPT API key required"}, status=400)

#             # Disconnect Pinecone first
#             Admin.objects.update(pinecone_token='')

#             # Connect ChatGPT API key
#             Admin.objects.update(openai_api_key=api_key)
#             return JsonResponse({"msg": "ChatGPT connected", "api_key": api_key})
#         except Exception as e:
#             return JsonResponse({"msg": str(e)}, status=500)

            