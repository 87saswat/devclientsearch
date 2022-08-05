

from django.forms import ModelForm
from .models import Projects, Review
from django import forms


class ProjectForm(ModelForm):
    class Meta:
        model = Projects
        fields = ['title', 'description',
                  'demmo_link', 'source_link', 'tags', 'featured_image']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update(
            {'class': 'input', 'placeholder': 'Add Title'}
        )
        self.fields['description'].widget.attrs.update(
            {'class': 'input', }
        )
        self.fields['title'].widget.attrs.update(
            {'class': 'input', 'placeholder': 'Add Title'}
        )
        self.fields['demmo_link'].widget.attrs.update(
            {'class': 'input', }
        )
        self.fields['source_link'].widget.attrs.update(
            {'class': 'input', }
        )
        self.fields['tags'].widget.attrs.update(
            {'class': 'input', }
        )
        self.fields['featured_image'].widget.attrs.update(
            {'class': 'input', }
        )

        # or put a for loop by
        # ----------------------------------------------------
        # for name, field in self.fields.items():
        #     field.widget.attrs.update({'class': 'input'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']

        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment to your vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget.attrs.update(
            {'class': 'input'}
        )
        self.fields['value'].widget.attrs.update(
            {'class': 'input'}
        )
