
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'videos', views.VideoViewSet)
router.register(r'comments', views.CommentViewSet)


urlpatterns = [
    path('', views.home_page, name='homepage'),
    path('videos', views.VideoListView.as_view(), name='videos'),
    path('comments', views.CommentListView.as_view(), name='comments'),
    path('video/', views.Videoview, name='video'),
    path('comment/', views.Commentview, name='comment'),
    path('api/', include(router.urls), name='api')
]