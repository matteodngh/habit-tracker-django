from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import HabitSerializer, DailyCheckSerializer, UserSerializer
from .models import Habit, DailyCheck
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class MailSender(APIView):
    def post(self, request, format=None):
        to_email = request.data.get("email")
        subject = request.data.get("subject")
        message = request.data.get("message")
        if User.objects.filter(email=to_email):
            return Response({"message": "e-mail already exists"},
                        status=status.HTTP_409_CONFLICT)
        send_mail(
            subject,
            message,
            'ultimoesamesac@gmail.com',
            [to_email],
            fail_silently=False,
        )
        return Response({"message": "e-mail has been sent successfully"},
                        status=status.HTTP_200_OK)

class MailSenderForgot(APIView):
    def post(self, request, format=None):
        to_email = request.data.get("email")
        subject = request.data.get("subject")
        message = request.data.get("message")
        if User.objects.filter(email=to_email):
            send_mail(
                subject,
                message,
                'ultimoesamesac@gmail.com',
                [to_email],
                fail_silently=False,
            )
            return Response({"message": "e-mail has been sent successfully"},
                        status=status.HTTP_200_OK)

class MailSenderForgot(APIView):
    def post(self, request, format=None):
        to_email = request.data.get("email")
        subject = request.data.get("subject")
        message = request.data.get("message")
        if User.objects.filter(email=to_email):
            send_mail(
                subject,
                message,
                'ultimoesamesac@gmail.com',
                [to_email],
                fail_silently=False,
            )
            return Response({"message": "e-mail has been sent successfully"},
                        status=status.HTTP_200_OK)

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'user_name': user.username
        })


class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['created_by']


class DailyCheckViewSet(viewsets.ModelViewSet):
    queryset = DailyCheck.objects.all()
    serializer_class = DailyCheckSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['date', 'habit']

    def create(self, request, *args, **kwargs):
        response = {'message': 'You cant create dailychecks like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
