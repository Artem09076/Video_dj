from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"videos", views.VideoViewSet)
router.register(r"comments", views.CommentViewSet)

from drf_yasg.views import get_schema_view 
from drf_yasg import openapi
from django.views.generic import TemplateView


schema_view = get_schema_view(  # new
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    # url=f'{settings.APP_URL}/api/v3/',
    patterns=[path('api/', include(router.urls)), ],
    public=True,
    permission_classes=(views.MyPermission,),
)


urlpatterns = [
    path('swagger-ui/', TemplateView.as_view(template_name='swaggerui/swaggerui.html', extra_context={'schema_url': 'openapi-schema'}), name='swagger-ui'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path("", views.home_page, name="homepage"),
    path("videos/", views.VideoListView.as_view(), name="videos"),
    path("comments/", views.CommentListView.as_view(), name="comments"),
    path("video/", views.Videoview, name="video"),
    path("comment/", views.Commentview, name="comment"),
    path("api/", include(router.urls), name="api"),
]
