from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    avatar_url = serializers.SerializerMethodField()
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name',
                  'phone', 'student_id', 'department', 'user_type',
                  'avatar', 'avatar_url', 'bio', 'is_staff', 'is_active',
                  'date_joined', 'created_at', 'items_count']
        extra_kwargs = {'avatar': {'write_only': True}}

    def get_avatar_url(self, obj):
        request = self.context.get('request')
        if obj.avatar and request:
            return request.build_absolute_uri(obj.avatar.url)
        return None

    def get_items_count(self, obj):
        # Use annotated value if available, otherwise query
        if hasattr(obj, 'items_count'):
            return obj.items_count
        return obj.items.count()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2',
                  'first_name', 'last_name', 'phone', 'student_id',
                  'department', 'user_type']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password2': '两次密码不一致'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone',
                  'student_id', 'department', 'user_type', 'bio', 'avatar']
