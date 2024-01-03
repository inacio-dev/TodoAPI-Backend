from rest_framework import serializers
from .models import Task
from user.models import Account

class TaskSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=Account.objects.all(), required=False)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'completed', 'user']

