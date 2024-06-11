"""This module include path."""
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('videos', views.VideoViewSet)
router.register('comments', views.CommentViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title='Snippets API',
        default_version='v1',
        description='Test description',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='contact@snippets.local'),
        license=openapi.License(name='BSD License'),
    ),
    patterns=[
        path('api/', include(router.urls)),
    ],
    public=True,
    permission_classes=(views.MyPermission,),
)


urlpatterns = [
    path(
        'swagger/',
        TemplateView.as_view(
            template_name='swaggerui/swaggerui.html',
            extra_context={'schema_url': 'openapi-schema'},
        ),
        name='swagger-ui',
    ),
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    path('', views.home_page, name='homepage'),
    path('videos/', views.users_video_catalog, name='videos'),
    path('comments/', views.user_comment_catalog, name='comments'),
    path('video/', views.video_view, name='video'),
    path('comment/', views.home_page, name='comment'),
    path('api/', include(router.urls), name='api'),
    path('register/', views.register, name='register'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('result/', views.result_page, name='results'),
    path('account/', views.account_page, name='account'),
    path('account/video/upload', views.video_create, name='upload_video'),
    path('comments/<uuid:comment_id>/delete/', views.delete_comment, {'next_url': 'comments'}, name='delete_comment'),
    path('videos/<uuid:video_id>/delete/', views.delete_video, name='delete_video'),
    path('video/<uuid:comment_id>/delete/', views.delete_comment, {'next_url': '/video/?id={video_id}'}, name='delete_from_video'),
    path('video/<uuid:comment_id>/update/', views.comment_update, name='comment_update'),
]
