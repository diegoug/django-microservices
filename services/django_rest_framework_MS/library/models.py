from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _

LANGUAGE = (
    ('es', _('Spanish')),
    ('en', _('English')),
    ('fr', _('French')),
)

CATHEGORY = (
    ('romantic', _('Romantic')),
    ('terror', _('Terror')),
    ('adventure', _('Adventure')),
    ('science_fiction', _('Science fiction')),
)


class Book(models.Model):
    title = models.CharField(
        _("title"), max_length=100)
    author = models.ForeignKey(
        _('author'), related_name='author', on_delete=models.PROTECT)
    publication_date = models.DateField(
        _('publication_date'))
    language =  models.CharField(
        _('language'), max_length=2, choices=LANGUAGE)
    cathegory = models.CharField(
        _("cathegory"), max_length=15, choices=CATHEGORY)
    created = models.DateTimeField(
        _('Created'), auto_now_add=True)

    class Meta:
        verbose_name = _("book")
        verbose_name_plural = _("books")
    
    def __str__(self):
        return "{} - {}".format(self.title, self.author)


class Author(models.Model):
    full_name = models.CharField(
        _("name"), max_length=100)
    date_birth = models.DateField(
        _('date_birth'))
    
    class Meta:
        verbose_name = _("author")
        verbose_name_plural = _("authors")
    
    def __str__(self):
        return "{}".format(self.full_name)
