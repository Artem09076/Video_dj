from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import CharField, IntegerField, FileField, ModelForm, Textarea
from .models import Video, Comment


class RegistrationForm(UserCreationForm):
    first_name = CharField(max_length=100, required=True)
    last_name = CharField(max_length=100, required=True)
    email = CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

class AddVideoForm(ModelForm):
    name = CharField(max_length=100, required=True)
    during = IntegerField(max_value=120, required=True)
    video_file = FileField(required=True)
    description = CharField(max_length=1000, required=False, widget=Textarea)
    cover_video_file = FileField(required=False)

    class Meta:
        model = Video
        fields = [
            'name',
            'description',
            'during',
            'video_file',
            'cover_video_file'
        ]

class AddCommentForm(ModelForm):
    text = CharField(max_length=300, required=True)

    class Meta:
        model = Comment
        fields = [
            "text"
        ]