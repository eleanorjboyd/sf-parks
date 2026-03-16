from django.shortcuts import get_object_or_404, render

from .models import Category, Park


def park_list(request):
    categories = Category.objects.all()
    selected_slugs = request.GET.getlist("categories")
    search_query = request.GET.get("q", "").strip()

    parks = Park.objects.prefetch_related("categories").all()

    if search_query:
        parks = parks.filter(name__icontains=search_query)

    if selected_slugs:
        for slug in selected_slugs:
            parks = parks.filter(categories__slug=slug)
        parks = parks.distinct()

    return render(
        request,
        "parks/park_list.html",
        {
            "parks": parks,
            "categories": categories,
            "selected_slugs": selected_slugs,
            "search_query": search_query,
        },
    )


def park_detail(request, pk):
    park = get_object_or_404(Park.objects.prefetch_related("categories"), pk=pk)
    return render(request, "parks/park_detail.html", {"park": park})
