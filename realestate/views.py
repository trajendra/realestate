from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView,UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from cloudinary.forms import cl_init_js_callbacks      
from .models import Property_Ref
from .forms import Property_RefForm
from realestate.models import *

# Create your views here.

def upload(request):
    context = dict( backend_form = Property_RefForm())
    if request.method == 'POST':
        form = Property_RefForm(request.POST, request.FILES)
        context['posted'] = form.instance
        if form.is_valid():
            form.save()
    return render(request, 'property_ref_upload.html', context)

class PropList(ListView):
    model = Property
    template_name = "realestate/index.html"
    
    def get_header_data(self):
        self.promo_header = Property_Promo.objects.active()
        return self.promo_header
    
    def get_context_data(self,**kwargs):
        context_data = super(PropList,self).get_context_data(**kwargs)
        context_data['promo_header'] = self.get_header_data()
        return context_data


class PropDetail(DetailView):
    model = Property
    template_name = "realestate/detail.html"
    
    def get_ref_data(self):
        prop_slug = self.kwargs['slug']
        self.prop = get_object_or_404(Property,slug=prop_slug)
        self.prop_ref = Property_Ref.objects.filter(property=self.prop)
        return self.prop_ref
    
    def get_related_data(self):
        prop_slug = self.kwargs['slug']
        prop = get_object_or_404(Property,slug=prop_slug)
        return Property.objects.published().filter(type=prop.type).order_by('-created')[:10]
        
    def get_context_data(self,**kwargs):
        context_data = super(PropDetail,self).get_context_data(**kwargs)
        context_data['prop_ref'] = self.get_ref_data()
        context_data['related_entries'] = self.get_related_data() 
        return context_data
    

class PropTypeList(ListView):
    template_name = "realestate/prop_type_list.html"
    
    def get_queryset(self):
        prop_type=self.kwargs['slug']
        self.type=get_object_or_404(Property_Type, slug=prop_type)
        return Property.objects.filter(type=self.type)

@method_decorator(login_required, name='dispatch')
class ListingInterest(CreateView):
    model = Listing_Interest
    fields = ['message','contact_no']
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        listing_slug = self.kwargs['slug']
        form.instance.listing = get_object_or_404(Property,slug=listing_slug)
        form.instance.created = self.request.user
        return super(ListingInterest, self).form_valid(form)
        

        
    
    
    
    
        
    
    

    
