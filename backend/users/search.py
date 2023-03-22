from django_select2.forms import ModelSelect2Widget
from .models import User

class MyModelSelect2Widget(ModelSelect2Widget):
    search_fields = [
        'username__icontains',
        'first_name__icontains',
        'last_name__icontains',
        'bio__icontains'
        # Add any other fields to search here
    ]

    model = User
    queryset = User.objects.all()
