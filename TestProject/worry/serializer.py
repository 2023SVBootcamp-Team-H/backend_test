from rest_framework import serializers
from .models import Worry, Answer


class WorrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Worry
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'
