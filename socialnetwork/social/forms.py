from django import forms
from .models import Post, Comments, UserProfile, User

class PostForm(forms.ModelForm):
    body = forms.CharField(label='', max_length=300, widget=forms.Textarea(
        attrs={'rows':'3','placeholder':'What\'s on your mind?' }
    ))
    image = forms.ImageField(label='',required=False)
    class Meta:
        model = Post
        fields = ['body', 'image']

class CommentForm(forms.ModelForm):
    comment = forms.CharField(label='', max_length=300, widget=forms.Textarea(
        attrs={'rows':'3','placeholder':'Add a comment' }
    ))
    class Meta:
        model = Comments
        fields = ['comment']
        
class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(label='username', max_length=150)
    class Meta:
        model = User
        fields = ['username']

class ProfileUpdateForm(forms.ModelForm):
    name = forms.CharField(label='Name', max_length=150, required= False)
    bio = forms.CharField(label='Bio', max_length=300, required=False, widget=forms.Textarea(
        attrs={'rows':'3','placeholder':'What\'s on your mind?' }
    ))
    location = forms.CharField(label='location', max_length=150, required=False)
    picture = forms.ImageField(required=False)
    class Meta:
        model = UserProfile
        fields = ['name', 'bio','location', 'picture']