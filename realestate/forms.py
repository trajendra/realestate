from django.forms import ModelForm      
from .models import Property_Ref

class Property_RefForm(ModelForm):
  class Meta:
      model = Property_Ref
      fields = '__all__'