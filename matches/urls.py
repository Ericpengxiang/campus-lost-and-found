from django.urls import path
from . import views

urlpatterns = [
    path('my/', views.MyMatchesView.as_view(), name='my_matches'),
    path('<int:pk>/', views.MatchDetailView.as_view(), name='match_detail'),
    path('run/<int:item_id>/', views.run_match, name='run_match'),
    path('admin/list/', views.AdminMatchListView.as_view(), name='admin_match_list'),
]
