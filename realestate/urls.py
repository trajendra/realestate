from django.conf.urls import url,include
from realestate.views import PropList,PropDetail,PropTypeList,ListingInterest,upload
from django.contrib import admin

urlpatterns = [
    url(r'^$', PropList.as_view(), name="home"),
    url(r'^(?P<slug>[\w\-]+)/$', PropDetail.as_view(), name="prop-detail"),
    url(r'^type/(?P<slug>[\w\-]+)/$', PropTypeList.as_view(), name="prop-type-list"),
    url(r'^(?P<slug>[\w\-]+)/interest/$', ListingInterest.as_view(), name="listing-interest"),
]

admin.site.site_header = 'Realestate'
admin.site.index_title = 'Realestate administration'
admin.site.site_title = 'Realestate Application'
