
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'surname', 'current_city', 'password', 'is_staff']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id', 'is_staff')

    def create(self, validated_data):
        print(validated_data)
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            name=validated_data['name'],
            surname=validated_data['surname'],
            current_city=validated_data['current_city'],
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
