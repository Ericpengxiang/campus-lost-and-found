from rest_framework import serializers
from .models import Item, ItemImage, Message
from users.serializers import UserSerializer


class ItemImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ItemImage
        fields = ['id', 'image', 'image_url', 'order']
        extra_kwargs = {'image': {'write_only': True}}

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None


class ItemListSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    first_image = serializers.SerializerMethodField()
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'user', 'type', 'type_display', 'title', 'category',
                  'category_display', 'location', 'happened_at', 'status',
                  'status_display', 'view_count', 'first_image', 'created_at']

    def get_first_image(self, obj):
        request = self.context.get('request')
        img = obj.images.first()
        if img and request:
            return request.build_absolute_uri(img.image.url)
        return None


class ItemDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    images = ItemImageSerializer(many=True, read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'user', 'type', 'type_display', 'title', 'category',
                  'category_display', 'description', 'location', 'happened_at',
                  'contact_phone', 'contact_wechat', 'status', 'status_display',
                  'view_count', 'is_approved', 'images', 'created_at', 'updated_at']


class ItemCreateSerializer(serializers.ModelSerializer):
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Item
        fields = ['type', 'title', 'category', 'description', 'location',
                  'happened_at', 'contact_phone', 'contact_wechat', 'uploaded_images']

    def create(self, validated_data):
        images = validated_data.pop('uploaded_images', [])
        item = Item.objects.create(**validated_data)
        for i, img in enumerate(images):
            ItemImage.objects.create(item=item, image=img, order=i)
        return item


class MessageSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)
    to_user_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Message
        fields = ['id', 'item', 'from_user', 'to_user', 'to_user_id',
                  'content', 'is_read', 'created_at']
        read_only_fields = ['item', 'from_user', 'to_user', 'is_read']
