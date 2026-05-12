from django.shortcuts import render, get_object_or_404
from .models import Package, Category
from django.db.models import Q

def packages_list(request):
    query = request.GET.get('q', '')
    category_name = request.GET.get('category', '')
    
    packages = Package.objects.all().order_by('-created_at')
    
    if query:
        packages = packages.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(hotel_details__icontains=query)
        )
        
    if category_name:
        packages = packages.filter(category__name__icontains=category_name)
        
    categories = Category.objects.all()
    
    context = {
        'packages': packages,
        'categories': categories,
        'query': query,
        'selected_category': category_name
    }
    return render(request, 'packages/list.html', context)

def package_detail(request, pk):
    package = get_object_or_404(Package, pk=pk)
    return render(request, 'packages/detail.html', {'package': package})
