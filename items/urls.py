from django.urls import path
from . import views

urlpatterns = [
    path('', views.ItemListView.as_view(), name='item_list'),
    path('create/', views.ItemCreateView.as_view(), name='item_create'),
    path('my/', views.MyItemsView.as_view(), name='my_items'),
    path('<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('<int:pk>/edit/', views.ItemUpdateDeleteView.as_view(), name='item_update'),
    path('<int:item_id>/messages/', views.ItemMessageListView.as_view(), name='item_messages'),
    path('admin/list/', views.AdminItemListView.as_view(), name='admin_item_list'),
    path('admin/stats/', views.admin_stats, name='admin_stats'),
    path('admin/<int:pk>/', views.AdminItemDetailView.as_view(), name='admin_item_detail'),
]
