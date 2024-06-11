"""This module include django form."""
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import (CharField, FileField, IntegerField, ModelForm,
                          Textarea)

from .models import Comment, Video

MAX_LENGTH_VIDEO = 120
MAX_LENGTH_COMMENT = 300


class RegistrationForm(UserCreationForm):
    """Registration user form.

    Args:
        UserCreationForm (_type_): django user creation form
    """

    first_name = CharField(max_length=MAX_LENGTH_VIDEO, required=True)
    last_name = CharField(max_length=MAX_LENGTH_VIDEO, required=True)
    email = CharField(max_length=MAX_LENGTH_VIDEO, required=True)

    class Meta:
        """Meta class for RegistrationForm."""

        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]


class AddVideoForm(ModelForm):
    """Form for video add.

    Args:
        ModelForm: django model form
    """

    name = CharField(max_length=MAX_LENGTH_VIDEO, required=True)
    during = IntegerField(max_value=MAX_LENGTH_VIDEO, required=True)
    video_file = FileField(required=True)
    description = CharField(max_length=1000, required=False, widget=Textarea)
    cover_video_file = FileField(required=False)

    class Meta:
        """Meta class for AddVideoForm."""

        model = Video
        fields = [
            'name',
            'description',
            'during',
            'video_file',
            'cover_video_file',
        ]


class AddCommentForm(ModelForm):
    """Form for add comment.

    Args:
        ModelForm: django model form
    """

    text = CharField(max_length=MAX_LENGTH_COMMENT, required=True)

    class Meta:
        """Meta class for AddCommentForm."""

        model = Comment
        fields = [
            'text',
        ]
