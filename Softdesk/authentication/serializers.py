
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, SerializerMethodField


User = get_user_model()


class RegisterSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        password=validated_data['password'],
                                        )
        return user