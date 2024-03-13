from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from items.models import Item


@login_required
def items_potions(request):
    all_items = Item.objects.order_by("id")

    context = {
        'all_items': all_items
    }
    return render(request, 'items/potions.html', context)
