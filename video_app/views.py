"""This module include views."""
import cv2
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.base import ContentFile
from django.core.paginator import Paginator
from django.http.request import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from rest_framework import authentication, permissions, viewsets

from .forms import AddCommentForm, AddVideoForm, RegistrationForm
from .models import Comment, CustomUser, Video
from .serializers import CommentSerializer, VideoSerializer


def extract_frame(video_path, num_frames: int = 1000):
    """Extract frame from video.

    Args:
        video_path : video path
        num_frames (int): num of frames. Defaults to 1000.

    Returns:
        Image or none
    """
    vidcap = cv2.VideoCapture(video_path)
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, num_frames)
    success, image = vidcap.read()
    if success:
        return image
    return None


def home_page(request: HttpRequest):
    """Create a home page view for site.

    Args:
        request (HttpRequest): request

    Returns:
        Render template for home page
    """
    paginator = Paginator(Video.objects.all(), 2)
    num_page = request.GET.get('page', 1)
    videos = paginator.get_page(num_page)
    return render(
        request,
        'home_page.html',
        context={
            'videos': videos,
            'p': paginator,
        },
    )


@login_required
def users_video_catalog(request: HttpRequest):
    """Create user catolog video view.

    Args:
        request (HttpRequest): request

    Returns:
        Render template for users video catalog page
    """
    user_id = CustomUser.objects.all().get(user=request.user.id).id
    instances = Video.objects.filter(user=user_id)
    paginator = Paginator(instances, 5)
    num_page = request.GET.get('page', 1)
    videos = paginator.get_page(num_page)
    return render(request, 'catalog/videos.html', context={'videos': videos, 'p': paginator})


@login_required
def user_comment_catalog(request: HttpRequest):
    """Create a user comment catalog page.

    Args:
        request (HttpRequest): request

    Returns:
        Render template for users comment catalog page
    """
    if request.method == 'GET':
        user_id = CustomUser.objects.all().get(user=request.user.id).id
        instances = Comment.objects.all().filter(user=user_id)
        return render(request, 'catalog/comments.html', context={'comments_list': instances})


@login_required
def delete_comment(request: HttpRequest, comment_id, next_url: str):
    """Delete user comment by id.

    Args:
        request (HttpRequest): request
        comment_id (_type_): comment id
        next_url (str): url for redirect

    Returns:
        Page video or comments user catalog
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    if '?' in next_url:
        next_url = next_url.format(video_id=comment.video.id)
    return redirect(next_url)


def video_view(request: HttpRequest):
    """Create video page.

    Args:
        request (HttpRequest): request

    Returns:
        Render template with video
    """
    errors = ''
    target_id = request.GET.get('id', '')
    video = Video.objects.get(id=target_id) if target_id else None
    comments = Comment.objects.all().filter(video=video.id) if video is not None else None
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            user = CustomUser.objects.all().get(user=request.user.id)
            Comment.objects.create(text=text, user=user, video=video)

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
            'form': form,
            'errors': errors,
        },
    )


def result_page(request: HttpRequest):
    """Create result page.

    Args:
        request (HttpRequest): request

    Returns:
        Render page with result
    """
    query = request.GET.get('q')
    result_query = Video.objects.filter(name__icontains=query)
    return render(
        request,
        'result.html',
        {'videos': result_query},
    )


def register(request: HttpRequest):
    """Create register page.

    Args:
        request (HttpRequest): request

    Returns:
        Redirect to homepage or render register page
    """
    errors = ''
    if request.method == 'POST':
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
        'forms/register.html',
        {
            'form': form,
            'errors': errors,
        },
    )


def log_in(request: HttpRequest):
    """Create login page.

    Args:
        request (HttpRequest): request

    Returns:
        Render template with login page
    """
    if request.method == 'GET':
        form = AuthenticationForm()
        return render(
            request,
            'forms/login.html',
            {
                'form': form,
            },
        )
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect('homepage')


def log_out(request: HttpRequest):
    """Logout user.

    Args:
        request (HttpRequest): request

    Returns:
        Redirect to homepage
    """
    logout(request)
    return redirect('homepage')


safe_methods = 'GET', 'HEAD', 'OPTIONS'
unsafe_methods = 'POST', 'DELETE', 'PUT'


class MyPermission(permissions.BasePermission):
    """Class with my premissions.

    Args:
        permissions: Base django premissions
    """

    def has_permission(self, request: HttpRequest, _):
        """Check user premissions.

        Args:
            request (HttpRequest): request

        Returns:
            Bool user premissions.
        """
        if request.method in safe_methods:
            return bool(request.user and request.user.is_authenticated)
        elif request.method in unsafe_methods:
            return bool(request.user and request.user.is_superuser)
        return False


def create_viewsets(model_class, serailizer):
    """Create class viewset.

    Args:
        model_class : model class
        serailizer (_type_): serializer for model class

    Returns:
        Class viewset
    """
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
    """Create account page template.

    Args:
        request (HttpRequest): request

    Returns:
        Render template with account page
    """
    return render(request, 'account_page.html')


def video_create(request: HttpRequest):
    """Create video create template.

    Args:
        request (HttpRequest): request

    Returns:
        Render template with video create form
    """
    errors = ''
    if request.method == 'POST':
        form = AddVideoForm(request.POST, request.FILES)
        if form.is_valid():
            user = CustomUser.objects.all().get(user=request.user.id)
            cover_video_file = form.cleaned_data['cover_video_file']
            video_name = form.cleaned_data['name']
            video_path = form.cleaned_data['video_file'].temporary_file_path()
            if cover_video_file is None:
                first_frame = extract_frame(video_path)
                _, buffer = cv2.imencode('.jpg', first_frame)
                frame_image = ContentFile(buffer.tobytes(), f'frame_for_video_{video_name}.jpg')
                form.cleaned_data['cover_video_file'] = frame_image
            Video.objects.create(**form.cleaned_data, user=user)
            return redirect('videos')

        else:
            errors = form.errors
    else:
        form = AddVideoForm()

    return render(
        request,
        'forms/upload_video.html',
        {
            'form': form,
            'errors': errors,
        },
    )


def delete_video(request: HttpRequest, video_id):
    """Deletre user video.

    Args:
        request (HttpRequest): request
        video_id (_type_): video id

    Returns:
        Redirect to videos page
    """
    video = get_object_or_404(Video, pk=video_id)
    video.delete()
    return redirect('videos')


def comment_update(request: HttpRequest, comment_id):
    """Update user comment.

    Args:
        request (HttpRequest): request
        comment_id (_type_): comment id

    Returns:
        Render template with update comment form or redirect to
    """
    errors = ''
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        form = AddCommentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('text')
            comment.text = text
            comment.save()
            q_video = f'?id={comment.video.id}'
            return redirect(reverse('video') + q_video)
        errors = form.errors
    else:
        form = AddCommentForm()
    return render(request, 'comment_update.html', {'form': form, 'errors': errors})
