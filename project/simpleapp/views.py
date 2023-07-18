
from django.contrib.auth.mixins import PermissionRequiredMixin
from datetime import datetime
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product
from .filters import ProductFilter
from .forms import ProductForm
from django.contrib.auth.mixins import LoginRequiredMixin


class ProductsList(ListView):
    model = Product
    ordering = 'name'
    # queryset = Product.objects.filter(
    #     price_lt=300
    # )
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = ProductFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class ProductDetail(DetailView):
    model = Product
    template_name = 'product.html'
    context_object_name = 'product'

class ProductCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('simpleapp.add_product',)
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'
# def create_product(request):
#     form = ProductForm()
#
#     if request.method == 'POST':
#         form = ProductForm(request.POST)
#         form.save()
#         return HttpResponseRedirect('/products/')


    # return render(request, 'product_edit.html', {'form': form})

class ProductUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('simpleapp.change_product',)
    form_class = ProductForm
    model = Product
    template_name = 'product_edit.html'

class ProductDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('simpleapp.delete_product',)
    model = Product
    template_name = 'product_delete.html'
    success_url = reverse_lazy('product_list')