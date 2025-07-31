from django import forms
from . import models

class CreatePost(forms.ModelForm):
    tags_input = forms.CharField(
        label="Tags (comma-separated)", required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Django, Python, AI'})
    )

    class Meta:
        model = models.Post
        fields = ['title', 'body', 'slug']

    def save(self, commit=True, user=None):
        post = super().save(commit=False)
        if user:
            post.author = user
        if commit:
            post.save()

        tags_raw = self.cleaned_data.get('tags_input', '')
        tag_names = [name.strip() for name in tags_raw.split(',') if name.strip()]

        tag_objs = []
        for name in tag_names:
            tag_obj, created = models.Tag.objects.get_or_create(name=name)
            tag_objs.append(tag_obj)

        post.tags.set(tag_objs)
        return post
    
class CreateComment(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={
                'class': 'comment-input',
                'placeholder': 'Add a comment...',
                'rows': 3,
            })
        }
