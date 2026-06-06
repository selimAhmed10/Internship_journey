from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.views import View
from django.http import JsonResponse
from .models import Account


# templete view(static)

"""
- No need to write any database queries only render the template
- Can only pass custom context data
- Minimal code just only template name
- Use without database data
"""
class HomeView(TemplateView):
    template_name='list.html'
    
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['infor'] ='Welcome - this is a static page'
        return context




# ListView
"""
- Automatic queryset handling and its build in for showing the objects list
- Automatic context variable and also support panignation
- Easy filtering and ordering and automatically show the objec list 
"""
class AccountListView(ListView):
    model=Account
    template_name='accounts/a.html'
    context_object_name='accounts'
    paginate_by=10 # 10 number of information will show it
    ordering=['-created_at']  #order it by the latest account craeted by the filed created 



# detailview 

"""
- Automatic 404 handling  if the object not found no need to use get_object_or_404
- use to show one objects details

"""
class AccountDetailView(DetailView):
    model=Account
    template_name='accounts/b.html'
    context_object_name='account'





# 4.createView 

"""
- Automatic form creation and validation 
- Saves data automatically and store it
"""
class AccountCreateView(CreateView):
    model=Account
    fields=['account_number','account_owner','account_type','balance']
    template_name='accounts/form.html'
    
    def form_valid(self, form):
        return super().form_valid(form)


# 5.  updateview

"""
- Automatically loads existing data into form validate it and then save it
- No need to write get and the post method
- Handles both display and update
"""

class AccountUpdateView(UpdateView):
    model=Account
    fields=['account_number','account_owner','account_type','is_active']
    template_name='accounts/form.html'


# DeleteView - Delete object

"""
- Automatic confirmation and delete it and also 404 handling
- No need to write delete logic
"""
class AccountDeleteView(DeleteView):
    model=Account
    template_name='accounts/c.html'
    success_url='/accounts/'


# View
"""
- Full control of request and response
- handle all crud operation but need to to many code
"""
class AccountBalanceView(View):
    def get(self,request,pk):
        account=Account.objects.get(pk=pk)
        return JsonResponse({'balance': str(account.balance)})
    
