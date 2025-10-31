from django.contrib import admin
from django.urls import path
from newapp.views import send_whatsapp_message
from newapp import views
from newapp.controllers.login import Logincontroller
from newapp.controllers.inbox import Inboxcontroller

from newapp.controllers.contact import Contactcontroller
from newapp.controllers.settings import Settingcontroller
from newapp.controllers.whatsapp import whatsappcontroller
from newapp.controllers.integration import Integrationcontroller
from newapp.views import whatsapp_templates
from newapp.controllers.integration import Integrationcontroller
integration_controller = Integrationcontroller()
from django.conf import settings
from django.conf.urls.static import static
from newapp.views import delete_pdf



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
    path('contact/tags/delete/<int:tag_id>/', views.delete_tag, name='delete_tag'),
    path('api/users/', views.user_search_api, name='user_search_api'),
    path('contact/edit/<int:id>/', Contactcontroller.edit_user, name='edit_user'),
    path('contact/delete/<int:id>/', Contactcontroller.delete_user, name='delete_user'),
    
    # setting
    path('settings/',Settingcontroller.dashboard , name='settings'),
   # channels
    path('setting/channels', Settingcontroller.channels_view, name='channels_view'),
    # integration
    path('setting/integration',Settingcontroller.integration,name='integration_view'),
    path('whatsapp_connect',whatsappcontroller.connect,name='whatsapp_connect'),
    #path('admin/connect_google_calendar/', Integrationcontroller.connect_google_calendar, name='connect_google_calendar'),
    #path('admin/disconnect_google_calendar/', Integrationcontroller.disconnect_google_calendar, name='disconnect_google_calendar'),

    
    
    # whatsapp
    path('get_message/', whatsappcontroller.get_message, name='get_message'),
    path('send_whatsapp_message/', whatsappcontroller.send_whatsapp_message,name='send_whatsapp_message'),
    path('disconnect/',whatsappcontroller.disconnect,name='disconnect'), 
    path('send_trigger/',whatsappcontroller.send_trigger,name='send_trigger'),
    path('appointment_date/',whatsappcontroller.appointment_date,name='appointment_date'),

    # Google Calendar event creation API endpoint
    path('create-event/', views.create_event_api, name='create_event_api'),
    
    
    
    # pinecone
    path('disconnect_pinecone/',Integrationcontroller.disconnect,name='disconnect'),
    path('connect_pinecone_token/',Integrationcontroller.connect,name='pinecone_connect'),
    
    
    path('flows/', views.flows_view, name='flows'),
    path('admin/', admin.site.urls),
   
    path('connect_whatsapp/', views.connect_whatsapp, name='connect_whatsapp'),
    path('voice_bot/', views.voice_bot, name='voice_bot'),
    path('send_voice_bot/', views.send_voice_bot, name='send_voice_bot'),
    
    path('show_people/',views.show_people,name='show_people'),
    path('chatbox/', views.show_chatbox, name='chatbox'),
    path('broadcast_msg/',views.broadcast_msg,name='broadcast_msg'),
    path('send_broadcast/', views.send_broadcast, name='send_broadcast'),
    path('import_contacts/', views.import_contacts, name='import_contacts'),
    path('api/whatsapp_templates/', whatsapp_templates, name='whatsapp_templates'),
    


    #chatgpt
    path('connect_openai_key/', views.connect_openai_key, name='connect_openai_key'),
    path('disconnect_openai_key/', views.disconnect_openai_key, name='disconnect_openai_key'),
    path('set_chatgpt_mode/', Integrationcontroller.set_chatgpt_mode, name='set_chatgpt_mode'),
    path('chatgpt_prompt/', views.chatgpt_prompt_page, name='chatgpt_prompt_page'),
    path('ai_agent/upload/', integration_controller.ai_agent_upload, name='ai_agent_upload'),
    path('ai_agent/delete/<int:pk>/', delete_pdf, name='delete_pdf'),
    path('whatsapp/chatgpt_webhook/', views.get_message_chatgpt, name='chatgpt_webhook'),
 


    # path('new/',views.new,name='new')  # ✅ This line is correct
    
]

if settings.DEBUG:  # Add this block at the bottom of the file
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)