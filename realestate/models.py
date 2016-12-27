from __future__ import unicode_literals

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify
from django.forms import ModelForm

from localflavor.in_.forms import INPhoneNumberField,INStateField,INZipCodeField

from cloudinary.models import CloudinaryField

import datetime
# Create your models here.

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]
    
def get_image_filename(instance, filename):
    try:
        slug = instance.slug
    except:
        slug = instance.property.slug
    return "gallery/property/images/%s-%s" % (slug, filename)  
    
class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    
    class Meta:
        abstract = True
        
class Agent(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.SET(get_sentinel_user), related_name="agent")
    photo = models.ImageField(upload_to='gallery/user/photo/%Y/%m/%d',
                               null=True,
                               blank=True,
                               help_text="Upload photo")
    address = models.TextField(blank=True, null=True)
    phone1 = models.CharField(max_length=15, blank=True, null=True)
    phone2 = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('agent_property_page',
                       kwargs={'username': self.user.username})

    class Meta:
        verbose_name = 'Property Agent'
        verbose_name_plural = 'Agents'
    

class Property_Type(models.Model):
    type = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100,unique=True)
    type_desc = models.CharField(max_length=200, blank=True, null = True)
    
    def __str__(self):
        return self.type
    
    def __unicode__(self):
        return self.type
    
    
class Tag(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title

    @property
    def get_total_properties(self):
        return Property.objects.filter(tags__pk=self.pk).count()

    class Meta:
        verbose_name = 'Detail Tag'
        verbose_name_plural = 'Tags'
        
class PropQuerySet(models.QuerySet):
    def published(self):
        return self.filter(publish=True)
    def active(self):
        return self.filter(is_active=True)

class Property(TimeStampedModel):
    LISTED, PENDING, SOLD = range(3)
    STATUS_CHOICES = (
        (LISTED,'Listed'),
        (PENDING,'Pending'),
        (SOLD,'Sold'),
        )
    agent = models.ForeignKey(Agent,on_delete=models.SET(get_sentinel_user),related_name="property_agent")
    type = models.ForeignKey(Property_Type,on_delete=models.SET(get_sentinel_user),related_name="ref_prop_type")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,unique=True)
    #cover = models.ImageField(upload_to=get_image_filename, null=True, blank=True,help_text='Optional cover for property')
    cover = CloudinaryField('image',null=True, blank=True,help_text='Optional cover for property')
    owner = models.CharField(max_length=100,blank=True, null=True)
    owner_contact = INPhoneNumberField()
    desc = models.TextField(blank=True, null=True)
    other_details = models.TextField(blank=True,null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=255,blank=True, null=True)
    state = INStateField()
    zip_code = INZipCodeField()
    room_count = models.PositiveSmallIntegerField(blank=True, null=True)
    vendor_requested_price = models.DecimalField(max_digits=20,decimal_places=2,blank=True, null=True)
    buyer_offered_price = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)
    agreed_selling_price = models.DecimalField(max_digits=20,decimal_places=2,blank=True, null=True)
    tags = models.ManyToManyField('Tag',blank=True)
    keywords = models.CharField(max_length=200, null=True, blank=True,help_text='Keywords sparate by comma.')
    meta_description = models.TextField(null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES,null=True, blank=True)
    publish = models.BooleanField(default=True)
    objects = PropQuerySet.as_manager()
    
    def get_absolute_url(self):
        return reverse('prop-detail', kwargs={'slug': self.slug})

    @property
    def total_visitors(self):
        return Visitor.objects.filter(property__pk=self.pk).count()

    def __str__(self):
        return self.title
        
    #def save(self):
    #    super(Property, self).save()
    #    date = datetime.date.today()
    #    self.slug = '%i-%i-%i-%s' % (
    #        date.year, date.month, date.day, slugify(self.title)
    #    )
    #    super(Property, self).save()

    class Meta:
        verbose_name = 'Detail Property'
        verbose_name_plural = 'Property'
        ordering = ["-created"]
        

class Property_Ref(TimeStampedModel):
    property = models.ForeignKey(Property,related_name="property_ref")
    #image = models.ImageField(upload_to=get_image_filename, verbose_name='Image')
    image = CloudinaryField('image')
    
    #def __str__(self):
    #    return self.property.title
    
    """ Informative name for mode """
    def __unicode__(self):
        try:
            public_id = self.image.public_id
        except AttributeError:
            public_id = ''
        return "Photo <%s:%s>" % (self.property.title, public_id)
    
class Visitor(TimeStampedModel):
    property = models.ForeignKey(Property, related_name='property_visitor')
    ip = models.CharField(max_length=40)

    def __str__(self):
        return self.property.title

    class Meta:
        verbose_name = 'Property Visitor'
        verbose_name_plural = 'Visitors'
        ordering = ['-created']

class Property_Promo(TimeStampedModel):
    #header = models.ImageField(upload_to='gallery/brand/header',null=True,blank=True,help_text="Upload header image for brand")
    header = CloudinaryField('promo',null=True,blank=True,help_text="Upload header image for brand")                           
    headline = models.CharField(max_length=300, null=True, blank=True)
    desc = models.TextField(null=True,blank=True)
    ref_url = models.ForeignKey(Property,blank=True,null=True)
    ref_url_info = models.CharField(max_length=25, default="More",null=True, blank=True)
    is_active = models.BooleanField(default=True)
    objects = PropQuerySet.as_manager()
    
    def __str__(self):
        return self.headline

class Listing_Interest(TimeStampedModel):
    user = models.ForeignKey(User,on_delete=models.SET(get_sentinel_user),related_name="user_interest")
    listing = models.ForeignKey(Property,on_delete=models.SET(get_sentinel_user),related_name="listing_interest")
    message = models.TextField(null=True,blank=True)
    contact_no = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        verbose_name = 'Listing Interested User'
        verbose_name_plural = 'Listing Interested Users'
        ordering = ['-created']
    
    def get_absolute_url(self):
        return reverse('prop-detail',kwargs={'slug': self.listing.slug})

class Listing_Rating(TimeStampedModel):
    user = models.ForeignKey(User,on_delete=models.SET(get_sentinel_user),related_name="user_rating")
    listing = models.ForeignKey(Property,on_delete=models.SET(get_sentinel_user),related_name="listing_rating")
    rating = models.PositiveSmallIntegerField(null=True,blank=True)


    
    

    
    
    
    
    
