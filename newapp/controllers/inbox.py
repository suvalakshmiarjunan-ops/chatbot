from django.http import HttpResponse
from django.shortcuts import render,redirect
from ..models import User
from ..models import Message
class Inboxcontroller:
    def dashboard(request):
        
        users = User.objects.only('id', 'phone_no').order_by('id')
        selected_user_id =  request.GET.get('user_id', '1')

        selected_user = None
        messages = []

        if selected_user_id:
            selected_user = User.objects.filter(id=selected_user_id).first()
            messages = Message.objects.filter(user_id=selected_user_id).order_by('created_at')

        return render(request, 'inbox/dashboard.html', {
            'users': users,
            'selected_user': selected_user,
            'messages': messages,
        })