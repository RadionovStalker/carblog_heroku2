import django_filters
from .models import Article, TreeCategory
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import get_language


class ArticleFilter(django_filters.FilterSet):

    CHOICE_LIST = (
        ('-like', _('Popular')),
        ('like', _('Unpopular')),
        ('-id', _('New')),
        ('id', _('Old'))
    )

    ordering = django_filters.ChoiceFilter(label=_("Show at first"), choices=CHOICE_LIST, method='filter_by_order')

    # tree_category = django_filters.NumberFilter(method='my_custom_filter')
    tree_category = django_filters.ModelMultipleChoiceFilter(queryset=TreeCategory.objects.all(),
                                             widget=forms.CheckboxSelectMultiple, method='my_custom_filter')
    class Meta:
        model = Article
        fields = ['tree_category']

    def filter_by_order(self, queryset, name, value):
        return queryset.order_by(value)

    def my_custom_filter(self, queryset, name, value):
        if len(value) > 0:
            categories = TreeCategory.objects.filter(name__in=value)
            ids_cat = list()
            for cat in categories:
                sub_categories = TreeCategory.get_tree(cat)
                for sub_cat in sub_categories:
                    if sub_cat.id not in ids_cat:
                        ids_cat.append(sub_cat.id)
            return queryset.filter(tree_category__id__in=ids_cat)
        else:
            return queryset
