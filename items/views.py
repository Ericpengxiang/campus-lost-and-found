from django.db.models import Q
from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Item, ItemImage, Message
from .serializers import (
    ItemListSerializer, ItemDetailSerializer,
    ItemCreateSerializer, MessageSerializer
)


class ItemListView(generics.ListAPIView):
    serializer_class = ItemListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Item.objects.filter(is_approved=True, status='active').select_related('user').prefetch_related('images')
        item_type = self.request.query_params.get('type')
        category = self.request.query_params.get('category')
        keyword = self.request.query_params.get('keyword')
        if item_type:
            qs = qs.filter(type=item_type)
        if category:
            qs = qs.filter(category=category)
        if keyword:
            qs = qs.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword) | Q(location__icontains=keyword))
        return qs

    def get_serializer_context(self):
        return {'request': self.request}


class ItemDetailView(generics.RetrieveAPIView):
    queryset = Item.objects.filter(is_approved=True).select_related('user').prefetch_related('images')
    serializer_class = ItemDetailSerializer
    permission_classes = [permissions.AllowAny]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        Item.objects.filter(pk=instance.pk).update(view_count=instance.view_count + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_context(self):
        return {'request': self.request}


class ItemCreateView(generics.CreateAPIView):
    serializer_class = ItemCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item = serializer.save(user=request.user)
        return Response(
            ItemDetailSerializer(item, context={'request': request}).data,
            status=status.HTTP_201_CREATED
        )


class ItemUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ItemCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Item.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        return Response(ItemDetailSerializer(instance, context={'request': request}).data)


class MyItemsView(generics.ListAPIView):
    serializer_class = ItemListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Item.objects.filter(user=self.request.user).select_related('user').prefetch_related('images')
        item_type = self.request.query_params.get('type')
        if item_type:
            qs = qs.filter(type=item_type)
        return qs

    def get_serializer_context(self):
        return {'request': self.request}


class ItemMessageListView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        item_id = self.kwargs['item_id']
        return Message.objects.filter(
            Q(item_id=item_id) & (Q(from_user=self.request.user) | Q(to_user=self.request.user))
        ).select_related('from_user', 'to_user')

    def perform_create(self, serializer):
        item_id = self.kwargs['item_id']
        to_user_id = self.request.data.get('to_user_id')
        from django.contrib.auth import get_user_model
        User = get_user_model()
        to_user = User.objects.get(pk=to_user_id)
        serializer.save(item_id=item_id, from_user=self.request.user, to_user=to_user)

    def get_serializer_context(self):
        return {'request': self.request}


# ─── Admin Views ─────────────────────────────────────────────────────────────

class AdminItemListView(generics.ListAPIView):
    serializer_class = ItemListSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        qs = Item.objects.all().select_related('user').prefetch_related('images')
        item_type = self.request.query_params.get('type')
        status_filter = self.request.query_params.get('status')
        keyword = self.request.query_params.get('keyword')
        if item_type:
            qs = qs.filter(type=item_type)
        if status_filter:
            qs = qs.filter(status=status_filter)
        if keyword:
            qs = qs.filter(Q(title__icontains=keyword) | Q(description__icontains=keyword))
        return qs

    def get_serializer_context(self):
        return {'request': self.request}


class AdminItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all().select_related('user').prefetch_related('images')
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ItemCreateSerializer
        return ItemDetailSerializer

    def get_serializer_context(self):
        return {'request': self.request}


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def admin_stats(request):
    from django.contrib.auth import get_user_model
    from matches.models import Match
    from django.db.models import Count
    User = get_user_model()
    # Category stats
    cat_qs = Item.objects.values('category').annotate(count=Count('id'))
    category_stats = {row['category']: row['count'] for row in cat_qs}
    return Response({
        'found_count': Item.objects.filter(type='found').count(),
        'lost_count': Item.objects.filter(type='lost').count(),
        'matched_count': Match.objects.filter(status='confirmed').count(),
        'user_count': User.objects.count(),
        'active_count': Item.objects.filter(status='active').count(),
        'closed_count': Item.objects.filter(status='closed').count(),
        'total_items': Item.objects.count(),
        'category_stats': category_stats,
    })
