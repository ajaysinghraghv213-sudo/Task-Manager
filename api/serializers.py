from .models import Tasks
from rest_framework import serializers
from django.contrib.auth.models import User
class TaskSerializers(serializers.ModelSerializer):
    class Meta:
        model=Tasks
        fields=['id','task','description','created_at','due_date','completed']
        read_only_fields = ['user']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','password']
    def create(self,validated_data):
        user=User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )            
        return user