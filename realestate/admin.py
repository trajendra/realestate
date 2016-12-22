from django.contrib import admin
from django import forms

from realestate.models import *
#import datetime
#now = datetime.datetime.now()

# Register your models here.
class PropertyRefInline(admin.TabularInline):
    model = Property_Ref
    extra = 1


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields ='__all__'

class PropertyAdmin(admin.ModelAdmin):
    form = PropertyForm
    fieldsets = (
        (None, {'fields':(('agent',))}),
        ('Property Type and Title Information', {'fields': (('type',),('title','slug',))}),
        ('Property Cover, Owner and address', {'fields': (('cover','owner',),('address',))}),
        ('Property Description', {'fields': (('room_count',),('desc',))}),
        ('Property Deal Details', {'fields': (('vendor_requested_price','buyer_offered_price'),('agreed_selling_price',))}),
        ('Tags & Keywords', {'fields': (('tags',),('keywords',))}),
        ('Meta Description for Search Engine Optimization', {'fields': ('meta_description',)}),
        ('Publish',{'fields':('publish',)})
    )
    inlines = (
        PropertyRefInline,
        
    )
    prepopulated_fields = {'slug': ('title',)}


# Register your models here.
admin.site.register(Agent)
admin.site.register(Property_Type)
admin.site.register(Property, PropertyAdmin)
admin.site.register(Property_Ref)
admin.site.register(Visitor)
admin.site.register(Tag)
admin.site.register(Property_Promo)
admin.site.register(Listing_Interest)
admin.site.register(Listing_Rating)
