from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from api.views import CustomObtainAuthToken, MailSender, MailSenderForgot

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', CustomObtainAuthToken.as_view()),
    path('send/', MailSender.as_view()),
    path('forgot/', MailSenderForgot.as_view()),
]
