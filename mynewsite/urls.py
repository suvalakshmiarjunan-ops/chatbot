from django.contrib import admin
from django.urls import path
from newapp.views import send_whatsapp_message
from newapp import views
from newapp.controllers.login import Logincontroller
from newapp.controllers.inbox import Inboxcontroller

from newapp.controllers.contact import Contactcontroller
from newapp.controllers.settings import Settingcontroller
from newapp.controllers.whatsapp import whatsappcontroller

from newapp import views


urlpatterns = [
    # logout
    path('',Logincontroller.enter,name=''),
    path('logout/',Logincontroller.logout,name='logout'),
    
    path('login_view/',Logincontroller.login_view),
    path('login_post/',Logincontroller.login_post,name='login_post'),
    
    path('dashboard/', views.dashboard_view, name='dashboard'),
    # inbox
    path('inbox/dashboard', Inboxcontroller.dashboard, name='inbox_dashboard'),
    
    # contact
    path('contact/dashboard',Contactcontroller.dashboard,name='contact_dashboard'),
    path('contact/add',Contactcontroller.add_user,name='add_user'),
    path('contact/add_admin_user',Contactcontroller.add_admin_user,name='add_admin_user'),
    path('contact/tag/', views.tag_view, name='add_tag'),

    
    
    # setting
    path('settings/',Settingcontroller.dashboard , name='settings'),
    # setting
    path('setting/channels', Settingcontroller.channels_view, name='channels_view'),

    path('settings/integrations/', views.integration_view, name='integration_view'),
    # path('settings/integrations/chatgpt/', views.chatgpt_integration, name='chatgpt_integration'),
    # path('chatgpt_integration/', views.chatgpt_integration, name='chatgpt_integration'),
    
    # path('chatgpt/respond/', views.chatgpt_respond, name='chatgpt_respond'),
    # channels
    path('whatsapp_connect',whatsappcontroller.connect,name='whatsapp_connect'),

    
    
    
    # whatsapp
    path('get_message/', whatsappcontroller.get_message, name='get_message'),
    path('send_whatsapp_message/', whatsappcontroller.send_whatsapp_message,name='send_whatsapp_message'),
    path('disconnect/',whatsappcontroller.disconnect,name='disconnect'), 
    
    path('flows/', views.flows_view, name='flows'),
    path('admin/', admin.site.urls),
   
    path('connect_whatsapp/', views.connect_whatsapp, name='connect_whatsapp'),
    path('voice_bot/', views.voice_bot, name='voice_bot'),
    path('send_voice_bot/', views.send_voice_bot, name='send_voice_bot'),
    
    path('show_people/',views.show_people,name='show_people'),
    path('chatbox/', views.show_chatbox, name='chatbox'),
    path('broadcast_msg/',views.broadcast_msg,name='broadcast_msg'),
    path('send_broadcast/', views.send_broadcast, name='send_broadcast'),
    


    # path('new/',views.new,name='new')  # ✅ This line is correct
]