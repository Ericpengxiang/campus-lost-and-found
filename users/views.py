from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, RegisterSerializer, UpdateProfileSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user, context={'request': request}).data,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }, status=status.HTTP_201_CREATED)


class MeView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UpdateProfileSerializer
        return UserSerializer

    def get_object(self):
        return self.request.user

    def get_serializer_context(self):
        return {'request': self.request}


class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def unread_count(request):
    from items.models import Message
    count = Message.objects.filter(to_user=request.user, is_read=False).count()
    return Response({'count': count})


class AdminUserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        from django.db.models import Count
        qs = User.objects.annotate(items_count=Count('items')).order_by('-date_joined')
        search = self.request.query_params.get('search')
        if search:
            from django.db.models import Q
            qs = qs.filter(Q(username__icontains=search) | Q(first_name__icontains=search))
        return qs

    def get_serializer_context(self):
        return {'request': self.request}


class AdminUserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_context(self):
        return {'request': self.request}
