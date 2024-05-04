from .models import User, Comment, Video
from django.views.generic import ListView
from rest_framework import permissions, viewsets, authentication
from .serializers import CommentSerializer, VideoSerializer, UserSerializer
from django.shortcuts import render, redirect
from typing import Any
from django.core.paginator import Paginator


def home_page(request):
    return render(
        request,
        "index.html",
        context={
            "comments": Comment.objects.count(),
            "videos": Video.objects.count(),
        },
    )


def create_listview(model_class, template, plural_name):
    class View(ListView):
        model = model_class
        template_name = template
        context_object_name = plural_name

        def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
            context = super().get_context_data(**kwargs)
            instances = model_class.objects.all()
            paginator = Paginator(instances, 10)
            page = self.request.GET.get("page")
            page_obj = paginator.get_page(page)
            context[f"{plural_name}_list"] = page_obj
            return context

    return View


VideoListView = create_listview(Video, "catalog/videos.html", "videos")
CommentListView = create_listview(Comment, "catalog/comments.html", "comments")
UserListView = create_listview(User, "catalog/users.html", "users")


def create_view(model_class, template, model_name):
    def view(request):
        target_id = request.GET.get("id", "")
        if request.user.is_authenticated:
            return render(
                request,
                template,
                context={
                    model_name: (
                        model_class.objects.get(id=target_id) if target_id else None
                    )
                },
            )
        return redirect("homepage")

    return view


Videoview = create_view(Video, "entities/video.html", "video")
Commentview = create_view(Comment, "entities/comment.html", "comment")


safe_methods = "GET", "HEAD", "OPTIONS"
unsafe_methods = "POST", "DELETE", "PUT"


class MyPermission(permissions.BasePermission):
    def has_permission(self, request, _):
        if request.method in safe_methods:
            return bool(request.user and request.user.is_authenticated)
        elif request.method in unsafe_methods:
            return bool(request.user and request.user.is_superuser)
        return False


def create_viewsets(model_class, serailizer):
    class ViewSet(viewsets.ModelViewSet):
        queryset = model_class.objects.all()
        serializer_class = serailizer
        permission_classes = [MyPermission]
        authentication_classes = [authentication.TokenAuthentication]

    return ViewSet


VideoViewSet = create_viewsets(Video, VideoSerializer)
CommentViewSet = create_viewsets(Comment, CommentSerializer)
UserViewSet = create_viewsets(User, UserSerializer)
