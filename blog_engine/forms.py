from django import forms
from django.core.exceptions import ValidationError
from .models import UserProfile
from django.contrib.auth.models import User
from .models import Article, Gallery
from tinymce.widgets import TinyMCE
from django.forms.models import inlineformset_factory
from parler.forms import TranslatableModelForm, TranslatedField
from django.utils.translation import gettext_lazy as _


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class UpdateArticleForm(TranslatableModelForm):
    title = TranslatedField()
    description = TranslatedField()
    body = TranslatedField(form_class=forms.CharField, widget=TinyMCEWidget(attrs={'required': False, 'cols': 30, 'rows': 10}))

    class Meta:
        model = Article
        fields = {
            'title',
            'description',
            'body',
            'tree_category',
            'image'
        }


class AddNewArticle(TranslatableModelForm):
    class Meta:
        model = Article
        fields = {
            'title',
            'description',
            'body',
            'tree_category',
            'image'
        }
    title = TranslatedField()
    description = TranslatedField()
    body = TranslatedField(form_class=forms.CharField,
                           widget=TinyMCEWidget(attrs={'required': False, 'cols': 30, 'rows': 10}))
    # body = forms.CharField(
    #     widget=TinyMCEWidget(
    #         attrs={'required': False, 'cols': 30, 'rows': 10}
    #     )
    # )
    image = TranslatedField(form_class=forms.ImageField(required=False))
    tree_category = TranslatedField()


class UpdateProfileFormView(forms.ModelForm):

    class Meta:
        model = User
        fields = {
            'first_name',
            'last_name',
            'email',
        }
    image = forms.ImageField()


CHOICE_LIST = (
    ('-like', _('Popular')),
    ('like', _('Unpopular')),
    ('-id', _('New')),
    ('id', _('Old'))
)


