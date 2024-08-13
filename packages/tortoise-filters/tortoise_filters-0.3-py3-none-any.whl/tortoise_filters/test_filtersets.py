from tortoise_filters.filterset import FilterSet
from tortoise_filters.models import User
from tortoise_filters.filter_fields import InFilter, CharFilter

class TestFilterSet(FilterSet):

    model = User

    users = InFilter(field_name="id", type_field=int)
    users2 = InFilter(field_name="id", type_field=str)
    users3 = CharFilter(field_name="name", lookup_expr="icontains")