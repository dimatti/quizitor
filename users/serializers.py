
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'surname', 'current_city', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print(validated_data)
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        print(validated_data)
        instance.name = validated_data.get('name', instance.name)
        instance.surname = validated_data.get('surname', instance.surname)
        instance.save()
        return instance
