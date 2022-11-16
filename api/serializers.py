from django.contrib.auth.hashers import make_password

from .models import Habit, DailyCheck
from rest_framework import serializers
from django.contrib.auth.models import User
from datetime import timedelta
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name']
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

class DailyCheckSerializer(serializers.ModelSerializer):
    habit_name = serializers.CharField(source='habit.title')
    habit_user = serializers.IntegerField(source='habit.created_by.id')
    class Meta:
        model = DailyCheck
        fields = ['id', 'date', 'done', 'habit_name', 'habit_user']


class HabitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Habit
        fields = ['id', 'title', 'description', 'public', 'sdate', 'edate', 'created_by']

    def create(self, validated_data):
        habit = Habit.objects.create(**validated_data)
        diff = abs((validated_data['sdate'] - validated_data['edate']).days)
        for i in range(0, diff + 1):
            DailyCheck.objects.create(date=(validated_data['sdate'] + timedelta(days=i)), habit=habit)
        return habit
