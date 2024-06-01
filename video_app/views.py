from django.contrib.auth import login, logout
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from rest_framework import authentication, permissions, viewsets
from django.http.request import HttpRequest
from .forms import RegistrationForm, AddVideoForm, AddCommentForm
from .models import Comment, CustomUser, Video, UserVideo
from .serializers import CommentSerializer, VideoSerializer
from django.contrib.auth.forms import AuthenticationForm

def home_page(request: HttpRequest):
    videos = Video.objects.all()
    return render(
        request,
        "home_page.html",
        context={
            "videos": videos,
        },
    )


def users_video_catalog(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect("homepage")
    user_id = CustomUser.objects.all().get(user=request.user.id).id
    instances = Video.objects.filter(customuser=user_id)
    return render(request, 'catalog/videos.html', context={'videos_list': instances})

def user_comment_catalog(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect("homepage")
    user_id = str(request.user.id)
    instances = Comment.objects.all().filter(user=user_id)
    return render(request, 'catalog/comments.html', context={'comments_list': instances})






def video_view(request: HttpRequest):
    target_id = request.GET.get("id", "")
    video =  Video.objects.get(id=target_id) if target_id else None
    comments = Comment.objects.all().filter(video=video.id) if video is not None else None
    if request.method == "POST":
        form = AddCommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            Comment.objects.create(text=text, user=request.user, video=video)

        else:
            errors = form.errors
    else:
        form = AddCommentForm()

    return render(
        request,
        'entities/video.html',
        context={
            'video': video,
            'comments': comments,
            'form': form
        },
    )



def result_page(request: HttpRequest):
    query = request.GET.get('q')
    result = Video.objects.filter(name__contains=query)
    return render(
        request,
        'result.html',
        {'videos':result}
    )


def register(request: HttpRequest):
    errors = ""
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            CustomUser.objects.create(user=user)
            login(request, user)
            return redirect('homepage')
        else:
            errors = form.errors
    else:
        form = RegistrationForm()

    return render(
        request,
        "forms/register.html",
        {
            "form": form,
            "errors": errors,
        },
    )

def log_in(request: HttpRequest):
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(
            request,
            'forms/login.html',
            {
                'form': form,
            }
        )
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect('homepage')

def log_out(request: HttpRequest):
    logout(request)
    return redirect('homepage')



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
        authentication_classes = [
            authentication.TokenAuthentication,
            authentication.BasicAuthentication,
        ]

    return ViewSet


VideoViewSet = create_viewsets(Video, VideoSerializer)
CommentViewSet = create_viewsets(Comment, CommentSerializer)

def account_page(request: HttpRequest):
    return render(request, 'account_page.html')

def video_create(request: HttpRequest):
    errors = ""
    if request.method == "POST":
        form = AddVideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save()
            user = CustomUser.objects.all().get(user=request.user.id)
            UserVideo.objects.create(user=user, video=video)
            return redirect('account')

        else:
            errors = form.errors
    else:
        form = AddVideoForm()

    return render(
        request,
        "forms/upload_video.html",
        {
            "form": form,
            "errors": errors,
        },
    )

