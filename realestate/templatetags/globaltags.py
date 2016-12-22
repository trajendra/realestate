from django import template
from realestate.models import Property_Type

register = template.Library()

@register.assignment_tag
def proptypes():
    type_queryset = Property_Type.objects.all()
    return type_queryset
