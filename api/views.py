import sys
import os
sys.path.append(os.path.abspath(os.path.pardir))
from .serializers import ArticleSerializer, UserProfileSerializer, ArticlePostSerializer, ArticlePutSerializer, \
    IntegerIdSerializer, ArticleDeleteSerializer
from rest_framework import generics
from blog_engine.models import Article, UserProfile, TreeCategory
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from django.utils import translation
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.serializers import ValidationError
from django.core.exceptions import PermissionDenied


class ArticleListAPI(generics.ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    name = 'article-list-api'


class ArticleLikeAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    name = "article-like-api"

    def post(self, request, **kwargs):
        id = IntegerIdSerializer(data=kwargs)
        if id.is_valid():
            try:
                art = Article.objects.get(id=id.data.get('id'))
            except ObjectDoesNotExist:
                return Response({"message": "Not found article with id={}".format(id.data.get('id'))}, status=404)
            if request.user in art.like.all():
                art.like.remove(request.user)
                return Response({"message": "Delete from favourite"}, status=200)
            else:
                art.like.add(self.request.user)
                return Response({"message": "Add to favourite"}, status=200)
        else:
            return Response({'message': "Invalid value of 'id', it must be integer positive number"}, status=400)


class ArticleDetailAPI(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    name = 'article-detail-api'

    def get(self, request):
        """curl http://127.0.0.1:8000/ru/api/article/?id=20"""
        id_art = IntegerIdSerializer(data=request.GET)
        if id_art.is_valid():
            article = Article.objects.filter(id=id_art.data.get('id'))
            if not article:
                return Response({"message": "Not found article with id={}".format(id_art.data.get('id'))}, status=404)
            else:
                serializer = ArticleSerializer(article, many=True)
                return Response({"data": serializer.data})
        else:
            return Response({'message': "Invalid value of 'id'={}, it must be integer positive number".format(id_art.data.get('id'))}, status=400)

    # добавить рассылку подписчикам
    def post(self, request):
        """>curl -X POST -H "Content-Type: application/json" -d "{\"title\":\"api\",\"description\":\"api\",\"body\":\"api\",\"tree_category\":\"1\",\"language\":\"en\"}" -u admin:qwerty12345  http://127.0.0.1:8000/ru
/api/article/
"""
        try:
            print(request)
            new_article = ArticlePostSerializer(data=request.data)
            print(new_article)
            new_article.is_valid(raise_exception=True)
            new_article.save(request)
            return Response({"message": "Successfully added"}, status=200)
        except ObjectDoesNotExist as error:
            return Response({"message": repr(error)}, status=404)
        except ValidationError as error:
            return Response({"message": repr(error)}, status=400)

    def put(self, request):
        """>curl -X PUT -H "Content-Type: application/json" -d "{\"id\":\"20\",\"title\":\"api update\",\"description\":\"api update\",\"body\":\"api update\",\"language\":\"en\"}" -u admin:qwerty12345  http://127.0.0
.1:8000/ru/api/article/
"""
        try:
            data_for_art = ArticlePutSerializer(data=request.data)
            data_for_art.is_valid(raise_exception=True)
            data_for_art.save(request)
            return Response({"message": "Successfully updated"}, status=200)
        except ObjectDoesNotExist as error:
            return Response({"message": repr(error)}, status=404)
        except ValidationError as error:
            return Response({"message": repr(error)}, status=400)
        except ValueError as error:
            return Response({"message": repr(error)}, status=400)
        except PermissionDenied as error:
            return Response({"message": repr(error)}, status=403)

    def delete(self, request):
        try:
            id = ArticleDeleteSerializer(data=request.data)
            id.is_valid(raise_exception=True)
            id.save(request)
            return Response({"message": "Successfully deleted"}, status=200)
        except PermissionDenied as error:
            return Response({"message": repr(error)}, status=403)
        except ValidationError as error:
            return Response({"message": repr(error)}, status=400)
        except ObjectDoesNotExist as error:
            return Response({"message": repr(error)}, status=404)


class UserProfileDetailAPI(generics.RetrieveAPIView):
    lookup_field = 'pk'
    name = 'user-detail-api'
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()


class UserProfileListAPI(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    name = 'user-list-api'


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    queryset = Article.objects.all()

    def get(self, request):
        return Response({
            'articles': reverse(ArticleListAPI.name, request=request),
            'authors': reverse(UserProfileListAPI.name, request=request)
        })
