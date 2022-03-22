from django import forms 

from .models import Post, Subscribe

class NewsPostForm(forms.ModelForm):
    # image = forms.ImageField(widget= forms.FileInput(}))

    class Meta:
        model = Post 
        exclude = ('slug','author')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        # self.fields['image'].widget.attrs.update({ "accept":"image/*"})

class SubscribeForm(forms.ModelForm):

    class Meta:
        model = Subscribe
        fields = ['name','email']