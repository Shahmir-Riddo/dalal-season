from django.shortcuts import render
from .models import Dalal
from .forms import DalalFilterForm
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
# Create your views here.
def index(request):
    form = DalalFilterForm(request.GET)
    dalals = Dalal.objects.all().order_by('-traitor_rank')
    if form.is_valid():
        search = form.cleaned_data['search']
        district = form.cleaned_data['district']
        status = form.cleaned_data['status']

        if search:
            dalals = dalals.filter(name__icontains=search)

        if district:
            dalals = dalals.filter(district=district)

        if status:
            dalals = dalals.filter(status=status)


    paginator = Paginator(dalals, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'page_obj': page_obj}
    
    context = {
        'page_obj': page_obj,
        'form': form,
    
    }
    return render(request, 'index.html', context)


def dalal_detail(request, id):
    dalal_obj = get_object_or_404(Dalal, id=id)
    context = {
        'dalal': dalal_obj
    }
    return render(request, 'dalal_detail.html', context)

@require_POST
def dalal_shoe_count(request):
    dalal_id = request.POST.get("dalal_id")
    dalal_obj = get_object_or_404(Dalal, id=dalal_id)
    Dalal.objects.filter(id=dalal_id).update(shoe_count=dalal_obj.shoe_count + 1)
    dalal_obj.refresh_from_db()
    return JsonResponse({"shoe_count": dalal_obj.shoe_count})

def dalal_ranking(request):
    dalals = Dalal.objects.filter(shoe_count__gt=1).order_by('-shoe_count')[:10]
    context = {'dalals': dalals}
    return render(request, 'dalal_ranking.html', context)