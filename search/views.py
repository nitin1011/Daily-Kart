from django.shortcuts import render
from django.views.generic import ListView
from products.models import Products
# Create your views here.


# class SearchProductView(ListView):
#     template_name = 'search/view.html'
#
#     def get_context_data(self, *args, **kwargs):
#         context = super(SearchProductView, self).get_context_data(*args, **kwargs)
#         query = self.request.GET.get('q')
#         context['query'] = query
#         return context
#
#     def get_queryset(self, *args, **kwargs):
#         request = self.request
#         method_dict = request.GET
#         query = method_dict.get('q', None)
#
#
#         if query is not None:
#             lookups = Q(product_name__icontains=query) | Q(product_category__icontains=query)
#             products = Products.objects.filter(lookups).distinct()
#             return products
#         return Products.objects.none()

def search(request):
    context = {}
    if request.method == 'GET':
        query = request.GET.get('q')
        query_list = query.split()
        context['query'] = query
        # lookups = Q(product_name__icontains=query) | Q(product_category__icontains=query)
        # products = Products.objects.filter(lookups).distinct()
        products = search_product(query_list)
        if len(products) == 0:
            context['empty'] = True
        else:
            context['empty'] = False
        context['object_list'] = products
        return render(request, 'search/view.html', context)
    else:
        return render(request, 'search/view.html', context)


def search_product(query_list):
    products = Products.objects.all()
    prod = []
    if len(query_list) == 0:
        return products
    else:
        for i in query_list:
            for j in range(len(products)):
                if (i.lower() in products[j].product_name.lower() or i.lower() in products[j].product_category.lower()) and products[j] not in prod:
                    prod.append(products[j])
        return prod
