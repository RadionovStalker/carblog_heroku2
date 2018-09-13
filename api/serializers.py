import sys
import os
sys.path.append(os.path.abspath(os.path.pardir))
from blog_engine.models import Article, UserProfile, Gallery, TreeCategory
from rest_framework import serializers
from django.contrib.auth.models import User
from parler_rest.serializers import TranslatableModelSerializer
from parler_rest.fields import TranslatedFieldsField
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import PermissionDenied


def validate_language(data):
    if 'language' in data.keys():
        lang = data['language']
        for lang_code, lang_name in settings.LANGUAGES:
            if lang_code == lang:
                return True
        else:
            raise serializers.ValidationError("Unsupported code of language={}".format(lang))


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'username',
            'last_name',
            'first_name',
            'email',
            # 'url'
        ]
        read_only_fields = ['username']
    # url = serializers.HyperlinkedIdentityField(
    #     view_name='user-detail-api',
    #     lookup_field='pk',
    # )


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = [
            'user',
            'image',
            'url',
        ]
        read_only_fields = ['url', 'image']
        # image = serializers.Field('image.url')
    user = UserSerializer()
    # image = serializers.ImageField(max_length=None, use_url=True)

    url = serializers.HyperlinkedIdentityField(
        view_name='user-detail-api',
        lookup_field='pk',
    )


class GallerySerializer(serializers.ModelSerializer):

    class Meta:
        model = Gallery
        fields = ('image', )
        read_only_fields = ['image']


class TreeCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TreeCategory
        fields = ('name')


class ArticlePostSerializer(serializers.Serializer):
    tree_category = serializers.IntegerField()
    title = serializers.CharField( max_length=250)
    description = serializers.CharField(max_length=1000)
    body = serializers.CharField()
    language = serializers.CharField(max_length=2, required=False)

    def validate(self, data):
        if not validate_language(data):
            data['language'] = settings.PARLER_LANGUAGES['default']['fallbacks'][0]
            # так добавляется поле manyTomanyField
        try:
            cat = TreeCategory.objects.get(id=data['tree_category'])
            data['tree_category'] = cat
        except ObjectDoesNotExist as error:
            raise error
        return data

    def save(self, request):
        art = Article()
        art.set_current_language(self.validated_data['language'])
        art.title = self.validated_data['title']
        art.description = self.validated_data['description']
        art.body = self.validated_data['body']
        art.author = request.user
        art.save()
        # так добавляется поле manyTomanyField
        art.tree_category.add(self.validated_data['tree_category'])
        art.save()


class ArticlePutSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=250, required=False)
    description = serializers.CharField(max_length=1000, required=False)
    body = serializers.CharField(required=False)
    language = serializers.CharField(max_length=2)

    def validate(self, data):
        if validate_language(data):
            return data

    def save(self, request):
        art_for_upd = Article.objects.get(id=self.validated_data['id'])
        if art_for_upd.author != request.user:
                    raise PermissionDenied("Forbidden, only author of the article can update it")
        try:
            art_for_upd.translations.get(language_code=self.validated_data['language'])
            new_translation = False
            print("is translation")
        except ObjectDoesNotExist:
            print("no translation")
            # если перевода на указ. язык еще нет, должны быть переданы все поля модели
            new_translation = True
        art_for_upd.set_current_language(self.validated_data['language'])
        if 'title' in self.validated_data.keys():
            art_for_upd.title = self.validated_data['title']
            print("no raise except")
        elif new_translation:
            print("raise except")
            raise ValueError("Field 'title' is null, you must put parameter 'title'")
        if 'description' in self.validated_data.keys():
            art_for_upd.description = self.validated_data['description']
        elif new_translation:
            raise ValueError("Field 'description' is null, you must put parameter 'description'")
        if 'body' in self.validated_data.keys():
            art_for_upd.body = self.validated_data['body']
        elif new_translation:
            raise ValueError("Field 'body' is null, you must put parameter 'body'")
        art_for_upd.save()


class ArticleDeleteSerializer(serializers.Serializer):
    id = serializers.IntegerField()

    def save(self, request):
        art_for_del = Article.objects.get(id=self.validated_data['id'])
        if art_for_del.author != request.user:
            raise PermissionDenied("Forbidden, only author of the article can delete it")
        art_for_del.delete()


class IntegerIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class ArticleSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(shared_model=Article)
    class Meta:
        model = Article
        fields = (
            'id',
            'author',
            'translations',
            'tree_category',
            'image',
            'gallery',
            'likes'
        )
        read_only_fields = ['id', 'url', 'author', 'gallery', 'likes']

    likes = serializers.SerializerMethodField()

    def get_likes(self, obj):
        return obj.like.count()

    author = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    gallery = GallerySerializer(many=True)