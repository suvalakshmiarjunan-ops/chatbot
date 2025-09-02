from django.http import JsonResponse
from django.http import HttpResponse
from newapp.models import Admin
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST

class Integrationcontroller:
    def dissconnect(request):
       Admin.objects.update(pinecone_token='')
       return JsonResponse({
           'msg':'disconnected pinecone'
       })
    # @require_POST
    @csrf_exempt
    def connect(request):
            try:
                data = json.loads(request.body.decode("utf-8"))
                token = data.get("api_key") or ""
                if not token:
                    return JsonResponse({"msg": "API key required"}, status=400)
                Admin.objects.update(pinecone_token=token)
                return JsonResponse({
                    "msg": "connected",
                    "token": token
                })
            except Exception as e:
                return JsonResponse({"msg": str(e)}, status=500)

            