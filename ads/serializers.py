from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from ads.models import Ad, Category, Selection
from users.models import UserRoles, User
from users.serializers import UserInfoSerializer


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    author = UserInfoSerializer()

    class Meta:
        model = Ad
        fields = ['name', 'price', 'author', 'category']


class AdDetailSerializer(serializers.ModelSerializer):
    author = UserInfoSerializer()
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Ad
        fields = '__all__'


class SelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'


class SelectionCreateSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(), required=False)

    def create(self, validated_data):
        requests = self.context.get('request')
        if 'owner' not in validated_data:
            validated_data['owner'] = requests.user
        elif 'owner' in validated_data and requests.user.role == UserRoles.MEMBER and \
                requests.user != validated_data['owner']:
            raise ValidationError('Нет доступа')
        return super().create(validated_data)

    class Meta:
        model = Selection
        fields = '__all__'
