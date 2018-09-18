import datetime

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from tinymce.models import HTMLField
from treebeard.mp_tree import MP_Node
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext_lazy as _
import os
from django.dispatch import receiver


class TreeCategory(MP_Node):
    name = models.CharField(max_length=30, verbose_name=_("Name of category"))
    node_order_by = ['name']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


def unique_gallery_name_path(instance, filename):

    upload_to = 'images/gallery'
    type_name = filename.split('.')[-1]
    unique_time = str((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
    uni_name = '_'.join([str(instance.id)+"_gal", unique_time])
    filename = '{0}.{1}'.format(uni_name, type_name)
    return os.path.join(upload_to, filename)


def unique_name_and_path(instance, filename):
    """
    Именование загруженного изображения в вид:
        id_статьи+текущая_дата_в_милисекундах+формат
    """
    upload_to = 'images/articles'
    type_name = filename.split('.')[-1]
    unique_time = str((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
    uni_name = '_'.join([str(instance.id), unique_time])
    filename = '{0}.{1}'.format(uni_name, type_name)
    return os.path.join(upload_to, filename)


def avatar_name_and_path(instance, filename):
    """
    Генерация имени для аватаров пользователей в вид:
    Ник пользователя+тек. дата в мил.сек.+формат
    """
    upload_to = "images/profiles"
    type_name = filename.split('.')[-1]
    unique_time = str((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
    uni_name = '_'.join([str(instance.user.username), unique_time])
    filename = '{0}.{1}'.format(uni_name, type_name)
    return os.path.join(upload_to, filename)


class Article(TranslatableModel):

    author = models.ForeignKey(User, related_name="article_author", on_delete=models.CASCADE, help_text=_("Enter the author of article"), default=1)
    date_creation = models.DateTimeField(_('Date of creation'), auto_now_add=True, help_text=_("Date of creation"))
    date_updating = models.DateTimeField(_('Date of updating'), auto_now=True, help_text=_("Date of update"))
    like = models.ManyToManyField(User, _('Like'), blank=True)
    # image = models.ImageField(_('Image'), upload_to="images/articles", blank=True)
    image = models.ImageField(_('Image'), upload_to=unique_name_and_path, blank=True, help_text=_("Main image of your article"))

    tree_category = models.ManyToManyField(TreeCategory, _('Category'), help_text=_("Select categories"))

    translations = TranslatedFields(
        title=models.CharField(_('Title'), max_length=250, help_text=_("Write your name of article")),
        description=models.CharField(_('Description'), max_length=1000,
                                   help_text=_("Enter a little description of your article")),
        body=HTMLField(_('Body'), help_text=_("Write text of article here")),
    )

    def __str__(self):
        return ' '.join([self.title, self.author.username, str(self.date_creation)])

    def get_absolute_url(self):
        return reverse('article-detail', args=[str(self.id)])

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ['-id']


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comment', verbose_name=_("Article"))
    text = models.CharField(max_length=1024, help_text=_("Write your commentary here"), verbose_name=_("Text of comment"))
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name=_("Author"))
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name=_("Date of creation"), help_text=_("Date of creation"))
    date_updating = models.DateTimeField(auto_now=True, verbose_name=_("Date of update"), help_text=_("Date of update"))
    parent_comment = models.ForeignKey('Comment', related_name='com_parent', blank=True, null=True, on_delete=models.CASCADE)
    child_comments = models.ForeignKey('Comment', related_name='com_children', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return ' '.join([self.article.title, self.author.username, str(self.date_updating)])

    def get_absolute_url(self):
        return reverse('commentary', args=[str(self.id)])

    class Meta:
        ordering = ['-date_creation', 'author', 'article']
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")


class Gallery(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, default=0, related_name="gallery")
    image = models.ImageField(upload_to=unique_gallery_name_path, blank=True, null=True, verbose_name=_('image'))

    class Meta:
        ordering = ['id']
        verbose_name = _("Gallery")

    def __str__(self):
        return self.article.title


class Subscribers(models.Model):
    blogger = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscribers", verbose_name=_('author'))
    subscriber = models.EmailField(verbose_name=_("Email of subscriber"))

    class Meta:
        ordering = ['blogger', 'subscriber']
        verbose_name = _("Subscriber")
        verbose_name_plural = _("Subscribers")

    def __str__(self):
        return ' '.join([self.subscriber, self.blogger.username])


class UserProfile(models.Model):
    image = models.ImageField(upload_to=avatar_name_and_path, blank=True, null=True, verbose_name=_('Avatar'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _("UserProfile")
        verbose_name_plural = _("UserProfiles")


@receiver(models.signals.pre_save, sender=UserProfile)
def avatar_del_on_change(sender, instance, **kwargs):
    """
    Удаление аватара из папки /files/ при изменении профиля пользователя (если аватар также был изменен)
    """
    if not instance.pk:
        return False
    try:
        old_file = UserProfile.objects.get(pk=instance.pk).image
    except Exception:
        return False
    new_file = instance.image
    if not old_file == new_file:
        try:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
        except Exception:
            print("аватара, связанного с пользователем не обнаружено")


@receiver(models.signals.post_delete, sender=Gallery)
@receiver(models.signals.post_delete, sender=UserProfile)
@receiver(models.signals.post_delete, sender=Article)
def del_on_del(sender, instance, **kwargs):
    """
    Удаление изображения из папки /files/ при удалении статьи
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)


@receiver(models.signals.pre_save, sender=Article)
def del_on_change(sender, instance, **kwargs):
    """
    Удаление изображения из папки /media/ при изменении
    изображения в статье
    """
    if not instance.pk:
        return False
    try:
        old_file = Article.objects.get(pk=instance.pk).image
    except Exception:
        return False
    new_file = instance.image
    if not old_file == new_file:
        try:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)
        except Exception:
            print("файла, связанного со статьей нет")

