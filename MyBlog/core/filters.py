import django_filters
from .models import Post

class PostFilter(django_filters.FilterSet):
    from_date = django_filters.DateTimeFilter(field_name="date_created", lookup_expr="gte")
    to_date = django_filters.DateTimeFilter(field_name="date_created", lookup_expr="lte")
    content = django_filters.CharFilter(field_name='content', lookup_expr='icontains')
    category = django_filters.NumberFilter(field_name='category')

    class Meta:
        model = Post
        fields = ['category', 'date_created', 'content']