
from rest_framework import serializers
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework import filters

from .models import Book, Author


class OutputAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['full_name']


class OutputBookSerializer(serializers.ModelSerializer):
        author = OutputAuthorSerializer()
        class Meta:
            model = Book
            fields = ['id', 'title', 'author', 'publication_date', 'language', 
                      'cathegory']


class BookListAPI(ListModelMixin, GenericViewSet):
    """
    View to list all books in the system.
    """
    queryset = Book.objects.all()
    serializer_class = OutputBookSerializer
    search_fields = ['title', 'author__full_name']
    filter_backends = [filters.SearchFilter]

    def get_template_names(self):
        if self.action == 'list':
            return ['book_list.html']
    
    def list(self, request, *args, **kwargs):
        """
        Return a list of all books.
        """
        # here you can place business logic
        # I suggest importing a function from ./businnes.py
        return super().list(request, *args, **kwargs)
