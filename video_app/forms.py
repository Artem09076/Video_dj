from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import CharField, IntegerField, FileField, ModelForm
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
    during = IntegerField(max_value=120)
    video_file = FileField()

    class Meta:
        model = Video
        fields = [
            'name',
            'during',
            'video_file'
        ]

class AddCommentForm(ModelForm):
    text = CharField(max_length=300, required=True)

    class Meta:
        model = Comment
        fields = [
            "text"
        ]